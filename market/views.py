# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.utils.html import format_html
from django.http import HttpResponse

# Create your views here.
from models import Softener, Purifier, Drinking
from models import EquipmentCategories, Equipment
from models import VentilationSpec, HeatSpec, AirSpec, SoundOffSpec, StrongSpec, CircularSpec, HiddenSpec
from models import Maintenance, MaintenanceAuxiliary
from models import Agent
from models import Order, OrderAuxiliary
from region.models import Province, City, County
from region.views import China
from wechat.views import Wechat
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
import uuid
from datetime import datetime


def uuid2str(_uuid):
    return str(_uuid).replace("-", "")


def str2uuid(_str):
    return ""


def appliances(request):
    """
    ge水系列产品展示
    :param request:
    :return:
    """
    hidden_field = ('id', 'description', 'price')
    d = {}
    for iter_class in (Softener, Purifier, Drinking):
        fields = iter_class._meta.get_fields()  # 所有model fields
        values = iter_class.objects.all().values()  # 所有model 行
        items = []
        for field in fields:
            item = []
            if field.name in hidden_field:
                continue
            item.append(field.verbose_name)
            # equipment是外键
            if field.name == "equipment":
                for ob in iter_class.objects.all():
                    item.append(ob.equipment.identification)
            else:
                for value in values:
                    item.append(value[field.name])
            items.append(item)
        d[iter_class.__name__.lower()] = items

    return render_to_response('appliances_list.html', d)


def lifegear(request):
    """
    lifegear系列产品展示
    :param request:
    :return:
    """
    ventilation = EquipmentCategories.objects.filter(group="ventilation").values()
    aeration = EquipmentCategories.objects.filter(group="aeration").values()

    return render_to_response('equipment_list.html', {"ventilation": ventilation, "aeration": aeration})


def lifegear_sub(request, sub):
    """
    lifegear 子系列产品展示
    :param request:
    :param sub: 大类
    :return:
    """
    ec = EquipmentCategories.objects.get(redirect=sub)  # 获取对应的大类
    path = ec.image
    eq_set = ec.equipment_set.all()          # 获取大类所有型号
    equipment = eq_set.values("identification", "description")

    match = {"bd": "VentilationSpec", "ls": "VentilationSpec", "hbd": "VentilationSpec", "bd120": "VentilationSpec",
             "bd125": "VentilationSpec", "ss": "VentilationSpec", "wrv": "HeatSpec", "hrv": "HeatSpec",
             "glx": "AirSpec", "ev21": "SoundOffSpec", "ev28": "StrongSpec", "ecv": "CircularSpec", "hev": "HiddenSpec"}

    hidden_field = ('id', 'equipment', 'size')
    cls_fields = eval(match[sub])._meta.get_fields()
    fields = []
    for field in cls_fields:
        if field.name in hidden_field:
            continue
        fields.append(field)

    values = getattr(ec.equipment_set.all()[0], match[sub].lower() + "_set").values()
    items = []
    for value in values:
        item = []
        for field in fields:
            item.append(value[field.name])
        items.append(item)

    return render_to_response('equipment_sub_list.html', {"equipment": equipment, "spec_th": fields, "spec": items,
                                                          "path": path})


def get_devices():
    # GE
    values = Equipment.objects.filter(session="GE").values("identification", "name")
    appliance = []
    for value in values:
        item = (value["identification"], value["name"])
        appliance.append(item)

    # 乐奇
    values = Equipment.objects.filter(session="lifegear").values("identification", "name")
    equipment = []
    for value in values:
        item = (value["identification"], value["name"])
        equipment.append(item)

    return {"appliance": appliance, "equipment": equipment}


@csrf_exempt
def maintenance(request):
    # 选择产品型号后ajax局部刷新
    if request.method == 'POST':
        numbers = request.POST.getlist('numbers[]', [])
        return render_to_response('maintenance_choose.html', {"numbers": numbers})

    # province devices signature
    provinces = Province.objects.values("name")
    devices = get_devices()
    signature = Wechat().signature(request.build_absolute_uri())

    return render_to_response('maintenance.html', {"appliance": devices["appliance"], "equipment": devices["equipment"],
                                                   "provinces": provinces, "signature": signature})


@csrf_exempt
def cities(request):
    province = Province.objects.get(name=request.POST.get("province", ""))
    city_list = province.city_set.all()
    return render_to_response('cities.html', {"cities": city_list})


@csrf_exempt
def counties(request):
    city = City.objects.get(name=request.POST.get("city", ""))
    county_list = city.county_set.all()
    return render_to_response('counties.html', {"counties": county_list})


class MaintenanceForm(forms.Form):
    name = forms.CharField(max_length=32, label="姓名")
    phone = forms.CharField(max_length=16, label="电话号码")
    fix_address = forms.CharField(max_length=64, label="安装地址")
    fix_date = forms.DateField(label="安装日期")
    devices = forms.CharField(max_length=256, label="设备列表")

    @classmethod
    def errors_label(cls, msg):
        for key in cls.declared_fields.keys():
            msg = msg.replace(key, cls.declared_fields[key].label)

        return format_html(msg)

    def clean_phone(self):
        """
        检查输入的手机号码，小于11位无效
        :return:
        """
        try:
            phone = self.cleaned_data['phone']
            if len(phone) < 11:
                raise ValueError()
        except Exception as e:
            raise forms.ValidationError("无效的电话号码")

        return phone

    def clean_fix_address(self):
        try:
            address = self.cleaned_data['fix_address']
            (province, city, county) = address.split(" ")
            Province.objects.get(name=province)
            City.objects.get(name=city)
            County.objects.get(name=county)
        except Exception as e:
            raise forms.ValidationError("无效的地址")

        return address

    # def clean_fix_date(self):
    #     try:
    #         import re
    #         dre = re.match("^20[0-2]\d-(0[1-9]|1[0-2])-([0-2]\d|3[01])$", d)
    #         return True if dre else False
    #
    #     except Exception as e:
    #         raise forms.ValidationError("无效的地址")
    #
    #     return address

    def clean_devices(self):
        """
        设备列表必须是json格式，每个列表编码必须有效
        :return: json格式的devices
        """
        try:
            devices = json.loads(self.cleaned_data['devices'])
            if not devices:
                raise ValueError()
            for device in devices:
                Equipment.objects.get(identification=device[0])
        except ValueError as e:
            raise forms.ValidationError("这个字段是必填项")
        except Exception as e:
            raise forms.ValidationError("无效的设备型号")

        return devices


@csrf_exempt
def maintenance_apply(request):
    f = MaintenanceForm(request.POST.copy())
    if f.is_valid():
        cd = f.cleaned_data
        guid = uuid.uuid1()
        now = datetime.now()

        try:
            for device in cd['devices']:
                equipment = Equipment.objects.get(identification=device[0])
                ma = MaintenanceAuxiliary(uuid=guid, equipment=equipment, number=device[1])
                ma.save()

            mas = MaintenanceAuxiliary.objects.filter(uuid=guid)
            m = Maintenance(name=cd['name'], phone=cd['phone'], fix_address=cd["fix_address"], fix_date=cd["fix_date"],
                            apply_time=now, uuid=guid, handled="no")
            m.save()

            # 多对多关系
            for ma in mas:
                m.auxiliary.add(ma)
            return render_to_response('maintenance_apply.html', {"yes": True})
        except Exception as e:
            return render_to_response('maintenance_apply.html', {"yes": False})
    else:
        return render_to_response('maintenance_apply.html', {"errors": MaintenanceForm.errors_label(str(f.errors))})


@csrf_exempt
def order(request):
    code = request.GET.get("code", None)
    if code:
        # 从微信菜单跳转过来
        openid = Wechat().openid(code)
    else:
        # 登录成功跳转
        openid = request.GET.get("openid", None)

    try:
        agent = Agent.objects.get(wechat=openid)
        provinces = Province.objects.values("name")
        devices = get_devices()
        return render_to_response("order.html", {"name": agent.name, "phone": agent.phone, "openid": openid,
                                                 'provinces': provinces, "appliance": devices['appliance'],
                                                 "equipment": devices['equipment']})
    except Exception as e:
        if openid:
            return render_to_response('login.html', {'openid': openid})
        else:
            return render_to_response('openid.html')


class AgentForm(forms.Form):
    name = forms.CharField(max_length=32, label="姓名")
    phone = forms.CharField(max_length=16, label="电话号码")
    openid = forms.CharField(max_length=64, label="openid")


@csrf_exempt
def login(request):
    # 登录，先保存Agent
    f = AgentForm(request.POST)
    if f.is_valid():
        try:
            cd = f.cleaned_data
            # 绑定合作伙伴openid
            agent = Agent.objects.get(name=cd['name'], phone=cd['phone'])
            agent.wechat = cd['openid']
            agent.save()

            return HttpResponse(json.dumps({"errcode": 0}), content_type="application/json")  # 前端跳转到/o
        except Exception as e:
            errors = "您不是有效的合作伙伴。"
            # return render_to_response('login.html', {"errors": errors, 'openid': cd['openid']})
            return HttpResponse(json.dumps({"errcode": 1, "msg": errors}), content_type="application/json")
    else:
        # errors = ["输入有误，请检查。"]
        # return render_to_response('login.html', {"errors": errors, 'openid': cd['openid']})
        errors = "请检查输入的信息。"
        if f["name"].errors:
            errors = "请输入有效的用户名。"
        elif f["phone"].errors:
            errors = "请输入有效的手机号码。"
        return HttpResponse(json.dumps({"errcode": 1, "msg": errors}), content_type="application/json")


class OrderForm(forms.Form):
    name = forms.CharField(max_length=32, label="姓名")
    phone = forms.CharField(max_length=16, label="电话号码")
    receipt_address = forms.CharField(max_length=64, label="收货地址")
    receipt_date = forms.DateField(label="到货日期")
    devices = forms.CharField(max_length=256, label="设备列表")
    openid = forms.CharField(max_length=64, label="openid")

    @classmethod
    def errors_label(cls, msg):
        for key in cls.declared_fields.keys():
            msg = msg.replace(key, cls.declared_fields[key].label)

        return format_html(msg)

    def clean_phone(self):
        """
        检查输入的手机号码，小于11位无效
        :return:
        """
        try:
            phone = self.cleaned_data['phone']
            if len(phone) < 11:
                raise ValueError()
        except Exception as e:
            raise forms.ValidationError("无效的电话号码")

        return phone

    def clean_receipt_address(self):
        try:
            address = self.cleaned_data['receipt_address']
            (province, city, county) = address.split(" ")
            Province.objects.get(name=province)
            City.objects.get(name=city)
            County.objects.get(name=county)
        except Exception as e:
            raise forms.ValidationError("无效的收货地址")

        return address

    def clean_devices(self):
        """
        设备列表必须是json格式，每个列表编码必须有效
        :return: json格式的devices
        """
        try:
            devices = json.loads(self.cleaned_data['devices'])
            if not devices:
                raise ValueError()
            for device in devices:
                Equipment.objects.get(identification=device[0])
        except ValueError as e:
            raise forms.ValidationError("这个字段是必填项")
        except Exception as e:
            raise forms.ValidationError("无效的设备型号")

        return devices


@csrf_exempt
def place_order(request):
    # 下订单
    f = OrderForm(request.POST.copy())
    if f.is_valid():
        cd = f.cleaned_data
        guid = uuid.uuid1()
        now = datetime.now()

        try:
            bill = 0
            oas = []
            for device in cd['devices']:
                equipment = Equipment.objects.get(identification=device[0])
                bill += int(equipment.price) * int(device[1])
                oa = OrderAuxiliary(uuid=guid, equipment=equipment, number=device[1])
                oas.append(oa)
                oa.save()
            bill *= 100  # 微信以分为单位
            if bill == 0:
                bill = 1

            agent = Agent.objects.get(name=cd['name'], phone=cd['phone'])
            m = Order(agent=agent, receipt_address=cd["receipt_address"], receipt_date=cd["receipt_date"],
                      order_time=now, uuid=guid, payed="no", shipped="no", valid="valid")
            m.save()

            # 多对多关系
            # oas = OrderAuxiliary.objects.filter(uuid=guid)
            for oa in oas:
                m.auxiliary.add(oa)

            return HttpResponse(json.dumps({"errcode": 0, "trade_no": uuid2str(guid), "bill": bill, "openid": cd["openid"]}),
                                content_type="application/json")
        except Exception as e:
            return HttpResponse(json.dumps({"errcode": 2, "msg": "未知错误，稍候重试"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"errcode": 1, "msg": OrderForm.errors_label(str(f.errors))}), content_type="application/json")


@csrf_exempt
def pay(request):
    signature = Wechat().signature(request.build_absolute_uri())
    name = "partner order"   # 合作伙伴下单
    trade_no = request.GET.get('no', '')
    fee = request.GET.get('bill', 0)
    openid = request.GET.get('openid', '')
    signature2 = Wechat().unified_order(name, trade_no, fee, request.META["REMOTE_ADDR"], openid)

    return render_to_response('pay.html', {"signature": signature, "signature_order": signature2, "trade_no": trade_no})


@csrf_exempt
def pay_notice(request):
    try:
        trade_no = Wechat().notice(request.body)
        if trade_no:
            trade = Order.objects.get(uuid=trade_no)
            trade.payed = "yes"
            trade.save()

        return render_to_response('notice_return.xml', content_type="application/xml")
    except Exception as e:
        return render_to_response('notice_return.xml', content_type="application/xml")


@csrf_exempt
def success(request):
    trade_no = request.GET.get('trade_no', '')
    return render_to_response('success.html')


def index(request):
    return render_to_response('index.html')


def china(request):
    try:
        China().load2mysql()
        return HttpResponse("导入成功")
    except Exception as e:
        return HttpResponse("导入失败")

def get_user(request):
    try:
        (appid, openid) = Wechat().fans()
        return render_to_response('user.html', {"appid": appid, "openids": openid})
    except Exception as e:
        return render_to_response('user.html')
