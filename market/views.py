# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response

# Create your views here.
from models import Softener, Purifier, Drinking
from models import EquipmentCategories, Equipment
from models import VentilationSpec, HeatSpec, AirSpec, SoundOffSpec, StrongSpec, CircularSpec, HiddenSpec
from models import Maintenance, MaintenanceAuxiliary
from region.models import Province, City, County
from django.views.decorators.csrf import csrf_exempt
from django import forms
import json
import uuid
from datetime import datetime


def appliances(request):
    """
    ge水系列产品展示
    :param request:
    :return:
    """
    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         # send_mail(
    #         #     cd['subject'],
    #         #     cd['message'],
    #         #     cd.get('email', 'noreply@example.com'),
    #         #     ['siteowner@example.com'],
    #         # )
    #         return HttpResponseRedirect('/contact/thanks/')
    # else:
    #     form = ContactForm(initial={'subject': 'I love your site!'})
    #
    # return render_to_response('appliances_list.html', {'form': form})
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
    # match = {"bd": "ventilationspec_set", "ls": "ventilationspec_set", "hbd": "ventilationspec_set",
    #          "bd120": "ventilationspec_set", "bd125": "ventilationspec_set", "ss": "ventilationspec_set",
    #          "wrv": "heatspec_set", "hrv": "heatspec_set", "glx": "airspec_set", "ev21": "soundoffspec_set",
    #          "ev28": "strongspec_set", "ecv": "circularspec_set", "hev": "hiddenspec_set"}
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


def index(request):
    return render_to_response('index.html')
