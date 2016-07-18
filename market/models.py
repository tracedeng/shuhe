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
    service_flow = models.CharField(max_length=16, verbose_name="服务流量")
    salt_tank_capacity = models.CharField(max_length=16, verbose_name="盐箱容量")
    resin_quantity = models.CharField(max_length=16, verbose_name="树脂数量")
    resin_tank_size = models.CharField(max_length=32, verbose_name="树脂罐尺寸")
    regeneration_time = models.CharField(max_length=16, verbose_name="再生时间")
    maximum_water_hardness = models.CharField(max_length=32, verbose_name="最大进水硬度")
    maximum_grains = models.CharField(max_length=16, verbose_name="最大格令数")
    maximum_iron_treatment = models.CharField(max_length=16, verbose_name="最大处理铁含量")

    class Meta:
        verbose_name_plural = "软水机"


class Purifier(Appliances):
    filtering_accuracy = models.CharField(max_length=16, verbose_name="过滤精度")
    rated_flow = models.CharField(max_length=16, verbose_name="额定流量")
    maximum_flow = models.CharField(max_length=16, verbose_name="最大流量")
    water_pressure = models.CharField(max_length=32, verbose_name="工作水压")
    water_temperature = models.CharField(max_length=32, verbose_name="工作水温")
    cartridge_life = models.CharField(max_length=32, verbose_name="滤芯寿命")

    class Meta:
        verbose_name_plural = "净水机"


class Drinking(Appliances):
    maximum_tds = models.CharField(max_length=16, verbose_name="最大TDS值")
    maximum_flow = models.CharField(max_length=32, verbose_name="最大流量")
    water_temperature = models.CharField(max_length=32, verbose_name="工作水温")
    water_pressure = models.CharField(max_length=32, verbose_name="工作水压")
    activated_carbon = models.CharField(max_length=32, verbose_name="前置活性碳")
    ro_film = models.CharField(max_length=32, verbose_name="Ro膜")

    class Meta:
        verbose_name_plural = "直饮机"


class Equipment(models.Model):
    identification = models.CharField(max_length=32, verbose_name="型号")
    description = models.CharField(max_length=64, verbose_name="型号描述")
    name = models.CharField(max_length=64, verbose_name="名称")

    class Meta:
        verbose_name_plural = "乐奇电器型号"


class VentilationSpec(models.Model):
    operation_mode = models.CharField(max_length=16, verbose_name="主操作模式")
    secondary_mode = models.CharField(max_length=16, verbose_name="二级操作模式")
    power_consumption = models.CharField(max_length=16, verbose_name="消耗电量")
    # price = models.BigIntegerField(verbose_name="价格")

    ventilation_volume = models.CharField(max_length=16, verbose_name="换气风量")
    air_volume = models.CharField(max_length=16, verbose_name="循环风量")
    noise = models.CharField(max_length=16, verbose_name="噪音")
    maximum_pressure = models.CharField(max_length=16, verbose_name="最大静压值")
    host_weight = models.CharField(max_length=16, verbose_name="主机重量")
    pipeline = models.CharField(max_length=16, verbose_name="连接管线")

    class Meta:
        verbose_name_plural = "乐奇换气设备规格"


class HeatSpec(models.Model):
    air_volume = models.CharField(max_length=16, verbose_name="风量")
    power_consumption = models.CharField(max_length=16, verbose_name="消耗电量")
    noise = models.CharField(max_length=16, verbose_name="噪音")
    recovery_rate = models.CharField(max_length=16, verbose_name="温度回收率")
    # price = models.BigIntegerField(verbose_name="价格")

    applicable_area = models.CharField(max_length=16, verbose_name="适用面积")
    host_size = models.CharField(max_length=16, verbose_name="主机尺寸")
    maximum_pressure = models.CharField(max_length=16, verbose_name="最大静压值")
    net_weight = models.CharField(max_length=16, verbose_name="净重")
    pipeline = models.CharField(max_length=16, verbose_name="进气管线排气管线")

    class Meta:
        verbose_name_plural = "新风全热空气净化机（交换机）设备规格"


class AirSpec(models.Model):
    host_size = models.CharField(max_length=16, verbose_name="主机尺寸")
    hoisting_size = models.CharField(max_length=16, verbose_name="吊装尺寸")
    # price = models.BigIntegerField(verbose_name="价格")

    air_volume = models.CharField(max_length=16, verbose_name="适用风量")
    weight = models.CharField(max_length=16, verbose_name="重量")
    pipeline = models.CharField(max_length=16, verbose_name="连接管线")

    class Meta:
        verbose_name_plural = "空气净化箱规格"


class Ventilator(models.Model):
    voltage = models.CharField(max_length=16, verbose_name="电压")
    power_consumption = models.CharField(max_length=16, verbose_name="消耗电量")
    ventilation_volume = models.CharField(max_length=16, verbose_name="换气风量")
    noise = models.CharField(max_length=16, verbose_name="噪音")
    # price = models.BigIntegerField(verbose_name="价格")

    maximum_pressure = models.CharField(max_length=16, verbose_name="最大静压值")
    # opening_size = models.CharField(max_length=16, verbose_name="开孔尺寸")
    host_weight = models.CharField(max_length=16, verbose_name="主机重量")
    pipeline = models.CharField(max_length=16, verbose_name="连接管线")

    class Meta:
        # verbose_name_plural = "换气扇规格"
        abstract = True


class SoundOffSpec(Ventilator):
    opening_size = models.CharField(max_length=16, verbose_name="开孔尺寸")

    class Meta:
        verbose_name_plural = "超静音换气扇规格"


class StrongSpec(Ventilator):
    opening_size = models.CharField(max_length=16, verbose_name="开孔/安装尺寸")

    class Meta:
        verbose_name_plural = "劲风换气扇规格"


class HiddenSpec(Ventilator):
    host_size = models.CharField(max_length=16, verbose_name="主机尺寸")

    class Meta:
        verbose_name_plural = "隐藏式换气扇规格"


class CircularSpec(models.Model):
    power_consumption = models.CharField(max_length=16, verbose_name="消耗功率")
    air_volume = models.CharField(max_length=16, verbose_name="风量")
    noise = models.CharField(max_length=16, verbose_name="噪音")
    installation_dimensions = models.CharField(max_length=16, verbose_name="安装尺寸")
    applicable_area = models.CharField(max_length=16, verbose_name="适用面积")
    weight = models.CharField(max_length=16, verbose_name="重量")

    class Meta:
        verbose_name_plural = "循环扇规格"


class Agent(models.Model):
    name = models.CharField(max_length=128, verbose_name="代理商")
    phone = models.CharField(max_length=32, verbose_name="代理商电话")
    wechat = models.CharField(max_length=64, verbose_name="代理商微信")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "合作伙伴"


class Maintenance(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    fix_address = models.CharField(max_length=32)
    fix_date = models.DateField()
    apply_time = models.TimeField()
    handled = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "官方维保"


class Order(models.Model):
    receipt_address = models.CharField(max_length=128)
    receipt_date = models.DateField()
    agent = models.ForeignKey(Agent)
    order_time = models.TimeField()
    payed = models.CharField(max_length=8)
    order_index = models.CharField(max_length=64)

    def __unicode__(self):
        return self.agent

    class Meta:
        verbose_name_plural = "订单"