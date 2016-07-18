# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response

# Create your views here.
from models import Softener, Purifier, Drinking


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