# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Appliances(models.Model):
    identification = models.CharField(max_length=64, verbose_name="设备编号")
    description = models.CharField(max_length=256, verbose_name="设备")
    price = models.BigIntegerField(verbose_name="价格")

    outline_dimension = models.CharField(max_length=64, verbose_name="外形尺寸")
    interface_size = models.CharField(max_length=32, verbose_name="接口尺寸")

    class Meta:
        abstract = True

    # def __unicode__(self):
    #     return u"%s %s" % (self.description, self.identification)


class Softener(Appliances):
    """软水机"""
    service_flow = models.CharField(max_length=16, verbose_name="服务流量")
    salt_tank_capacity = models.CharField(max_length=16, verbose_name="盐箱容量")
    resin_quantity = models.CharField(max_length=16, verbose_name="树脂数量")
    resin_tank_size = models.CharField(max_length=32, verbose_name="树脂罐尺寸")
    regeneration_time = models.CharField(max_length=16, verbose_name="再生时间")
    maximum_water_hardness = models.CharField(max_length=32, verbose_name="最大进水硬度")
    maximum_grains = models.CharField(max_length=16, verbose_name="最大格令数")
    maximum_iron_treatment = models.CharField(max_length=16, verbose_name="最大处理铁含量")


class Purifier(Appliances):
    filtering_accuracy = models.CharField(max_length=16, verbose_name="过滤精度")
    rated_flow = models.CharField(max_length=16, verbose_name="额定流量")
    maximum_flow = models.CharField(max_length=16, verbose_name="最大流量")
    water_pressure = models.CharField(max_length=32, verbose_name="工作水压")
    water_temperature = models.CharField(max_length=32, verbose_name="工作水温")
    cartridge_life = models.CharField(max_length=32, verbose_name="滤芯寿命")


class Drinking(Appliances):
    maximum_tds = models.CharField(max_length=16, verbose_name="最大TDS值")
    maximum_flow = models.CharField(max_length=32, verbose_name="最大流量")
    water_temperature = models.CharField(max_length=32, verbose_name="工作水温")
    water_pressure = models.CharField(max_length=32, verbose_name="工作水压")
    activated_carbon = models.CharField(max_length=32, verbose_name="前置活性碳")
    ro_film = models.CharField(max_length=32, verbose_name="Ro膜")


class Agent(models.Model):
    name = models.CharField(max_length=128, verbose_name="代理商")
    phone = models.CharField(max_length=32, verbose_name="代理商电话")
    wechat = models.CharField(max_length=64, verbose_name="代理商微信")

    def __unicode__(self):
        return self.name


class Maintenance(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    fix_address = models.CharField(max_length=32)
    fix_date = models.DateField()
    apply_time = models.TimeField()
    handled = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    receipt_address = models.CharField(max_length=128)
    receipt_date = models.DateField()
    agent = models.ForeignKey(Agent)
    order_time = models.TimeField()
    payed = models.CharField(max_length=8)
    order_index = models.CharField(max_length=64)

    def __unicode__(self):
        return self.agent