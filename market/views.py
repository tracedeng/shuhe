# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response

# Create your views here.
from models import Softener, Purifier, Drinking
from models import EquipmentCategories, Equipment
from models import VentilationSpec, HeatSpec, AirSpec, SoundOffSpec, StrongSpec, CircularSpec, HiddenSpec


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


def maintenance(request):
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

    if request.method == 'POST':
        if request.POST.get('numbers', ''):
            numbers = request.POST['numbers']
            return render_to_response('maintenance.html', {"appliance": appliance, "equipment": equipment, "numbers": numbers})
    return render_to_response('maintenance.html', {"appliance": appliance, "equipment": equipment})


def index(request):
    return render_to_response('index.html')
