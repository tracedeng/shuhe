# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect

# Create your views here.
from models import Softener, Purifier, Drinking
from models import EquipmentCategories, Equipment
from models import VentilationSpec, HeatSpec, AirSpec, SoundOffSpec, StrongSpec, CircularSpec, HiddenSpec
from models import Maintenance, MaintenanceAuxiliary
from models import Agent
from models import Order, OrderAuxiliary
from region.models import Province, City, County
from wechat.views import Wechat
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
import uuid
import httplib
from datetime import datetime


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
            for value in values:
                item.append(value[field.name])
            items.append(item)
        d[iter_class.__name__.lower()] = items

    return render_to_response('appliances_list.html', d)


def lifegear(request):
    """
    lifegear水系列产品展示
    :param request:
    :return:
    """
    ventilation = EquipmentCategories.objects.filter(group="ventilation").values()
    aeration = EquipmentCategories.objects.filter(group="aeration").values()

    return render_to_response('equipment_list.html', {"ventilation": ventilation, "aeration": aeration})


def lifegear_sub(request, sub):
    ec = EquipmentCategories.objects.get(redirect=sub)  # 获取对应的大类
    eq_set = ec.equipment_set.all()          # 获取大类所有型号
    equipment = eq_set.values("identification", "description")

    match = {"bd": "VentilationSpec", "ls": "VentilationSpec", "hbd": "VentilationSpec", "bd120": "VentilationSpec",
             "bd125": "VentilationSpec", "ss": "VentilationSpec", "wrv": "HeatSpec", "hrv": "HeatSpec",
             "glx": "AirSpec", "ev21": "SoundOffSpec", "ev28": "StrongSpec", "ecv": "CircularSpec", "hev": "HiddenSpec"}

    hidden_field = ('id', 'equipment')
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

    return render_to_response('equipment_sub_list.html', {"equipment": equipment, "spec_th": fields, "spec": items})


@csrf_exempt
def maintenance(request):
    # 选择产品型号后ajax局部刷新
    if request.method == 'POST':
        if request.POST.getlist('numbers[]', []):
            numbers = request.POST.getlist('numbers[]')
            return render_to_response('maintenance_choose.html', {"numbers": numbers})

    # province
    provinces = Province.objects.values("name")

    # GE
    appliance = []
    for iter_class in (Softener, Purifier, Drinking):
        values = iter_class.objects.values("identification", "description")  # 所有model 行
        for value in values:
            item = (value["identification"], value["description"])
            appliance.append(item)

    # 乐奇
    values = Equipment.objects.values("identification", "name")
    equipment = []
    for value in values:
        item = (value["identification"], value["name"])
        equipment.append(item)

    signature = Wechat().signature(request.build_absolute_uri())
    if signature:
        return render_to_response('maintenance.html', {"appliance": appliance, "equipment": equipment,
                                                       "provinces": provinces, "signature": signature})

    return render_to_response('maintenance.html', {"appliance": appliance, "equipment": equipment,
                                                   "provinces": provinces})


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
    phone = forms.CharField(max_length=16)
    fix_address = forms.CharField(max_length=64)
    fix_date = forms.DateField()
    devices = forms.CharField(max_length=256)


@csrf_exempt
def maintenance_apply(request):
    mutable_post = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    mutable_post["fix_date"] = datetime.strptime(mutable_post["fix_date"], "%Y-%m-%d").date()
    f = MaintenanceForm(mutable_post)
    if f.is_valid():
        cd = f.cleaned_data
        guid = uuid.uuid1()
        now = datetime.now()

        devices = json.loads(cd['devices'])
        for device in devices:
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
        errors = None
    else:
        errors = f.errors
    # device_number = models.ManyToManyField(MaintenanceAuxiliary, verbose_name="设备及数量")
    # print json.loads(request.POST.get('devices'))
    return render_to_response('maintenance_apply.html', {"yes": True, "errors": errors})


class AgentForm(forms.Form):
    name = forms.CharField(max_length=32, label="姓名")
    phone = forms.CharField(max_length=16)
    openid = forms.CharField(max_length=64)


def get_devices():
    # GE
    appliance = []
    for iter_class in (Softener, Purifier, Drinking):
        values = iter_class.objects.values("identification", "description")  # 所有model 行
        for value in values:
            item = (value["identification"], value["description"])
            appliance.append(item)

    # 乐奇
    values = Equipment.objects.values("identification", "name")
    equipment = []
    for value in values:
        item = (value["identification"], value["name"])
        equipment.append(item)

    return {"appliance": appliance, "equipment": equipment}


@csrf_exempt
def order(request):
    if request.method == 'GET':
        # 从微信菜单跳转过来
        # 获取openid
        code = request.GET.get("code")
        conn = httplib.HTTPSConnection("api.weixin.qq.com")
        url = "/sns/oauth2/access_token?appid=wxe577b89ef194f974&secret=22c12dfc8ab1f4717238e8a909947748" \
              "&code=%s&grant_type=authorization_code" % code
        conn.request("GET", url)
        res = conn.getresponse()
        if res.status == 200:
            result = json.loads(res.read())
            openid = result.get("openid", None)
            if openid:
                # 验证是否已经绑定的openid
                try:
                    agent = Agent.objects.get(wechat=openid)
                    provinces = Province.objects.values("name")
                    devices = get_devices()
                    return render_to_response("order.html", {"name": agent.name, "phone": agent.phone, "openid": openid,
                                                             'provinces': provinces, "appliance": devices['appliance'],
                                                             "equipment": devices['equipment']})
                except Exception as e:
                    return render_to_response('login.html', {'openid': openid})
            else:
                return render_to_response('login.html')

        return render_to_response('login.html')
    else:
        # 登录，先保存Agent
        f = AgentForm(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            # 验证伙伴
            try:
                agent = Agent.objects.get(name=cd['name'], phone=cd['phone'])
                agent.wechat = cd['openid']
                agent.save()

                provinces = Province.objects.values("name")
                devices = get_devices()
                return render_to_response("order.html", {"name": cd['name'], "phone": cd['phone'], "openid": cd['openid'],
                                                         'provinces': provinces,"appliance": devices['appliance'],
                                                         "equipment": devices['equipment']})
            except Exception as e:
                errors = ["您不是有效的合作伙伴。"]
                return render_to_response('login.html', {"errors": errors, 'openid': cd['openid']})
        else:
            return render_to_response('login.html')


class OrderForm(forms.Form):
    name = forms.CharField(max_length=32, label="姓名")
    phone = forms.CharField(max_length=16)
    openid = forms.CharField(max_length=64)
    receipt_address = forms.CharField(max_length=64)
    receipt_date = forms.DateField()
    devices = forms.CharField(max_length=256)


@csrf_exempt
def place_order(request):
    # 下订单
    mutable_post = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    mutable_post["receipt_date"] = datetime.strptime(mutable_post["receipt_date"], "%Y-%m-%d").date()
    f = OrderForm(mutable_post)
    if f.is_valid():
        cd = f.cleaned_data
        guid = uuid.uuid1()
        now = datetime.now()

        devices = json.loads(cd['devices'])
        bill = 0
        for device in devices:
            equipment = Equipment.objects.get(identification=device[0])
            bill = bill + equipment.price
            oa = OrderAuxiliary(uuid=guid, equipment=equipment, number=device[1])
            oa.save()

        agent = Agent.objects.get(name=cd['name'], phone=cd['phone'])
        m = Order(agent=agent, receipt_address=cd["receipt_address"], receipt_date=cd["receipt_date"],
                  order_time=now, uuid=guid, payed="no", shipped="no", valid="valid")
        m.save()

        # 多对多关系
        oas = OrderAuxiliary.objects.filter(uuid=guid)
        for oa in oas:
            m.auxiliary.add(oa)

        return {"error": 0, "trade_no": guid, "bill": bill, "openid": cd["openid"]}
    else:
        # errors = f.errors
        return {"error": 1}

    # return render_to_response('maintenance_apply.html', {"yes": True, "errors": errors})


@csrf_exempt
def pay(request):
    signature = Wechat().signature(request.build_absolute_uri())
    name = "合作伙伴下单"
    trade_no = request.GET.get('no', '')
    fee = request.GET.get('bill', 0)
    openid = request.GET.get('openid', '')
    signature2 = Wechat().unified_order(name, trade_no, fee, request.META.REMOTE_ADDR, openid)

    return render_to_response('pay.html', {"signature": signature, "signature_order": signature2})


def pay_notice(request):
    try:
        trade_no = Wechat.notice(request.POST)
        if trade_no:
            trade = Order.objects.get(uuid=trade_no)
            trade.payed = "yes"
            trade.save()
    except Exception as e:
        pass


def index(request):
    return render_to_response('index.html')
