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
        verbose_name_plural = "GE软水机"


class Purifier(Appliances):
    filtering_accuracy = models.CharField(max_length=16, verbose_name="过滤精度")
    rated_flow = models.CharField(max_length=16, verbose_name="额定流量")
    maximum_flow = models.CharField(max_length=16, verbose_name="最大流量")
    water_pressure = models.CharField(max_length=32, verbose_name="工作水压")
    water_temperature = models.CharField(max_length=32, verbose_name="工作水温")
    cartridge_life = models.CharField(max_length=32, verbose_name="滤芯寿命")

    class Meta:
        verbose_name_plural = "GE净水机"


class Drinking(Appliances):
    maximum_tds = models.CharField(max_length=16, verbose_name="最大TDS值")
    maximum_flow = models.CharField(max_length=32, verbose_name="最大流量")
    water_temperature = models.CharField(max_length=32, verbose_name="工作水温")
    water_pressure = models.CharField(max_length=32, verbose_name="工作水压")
    activated_carbon = models.CharField(max_length=32, verbose_name="前置活性碳")
    ro_film = models.CharField(max_length=32, verbose_name="Ro膜")

    class Meta:
        verbose_name_plural = "GE直饮机"


class EquipmentCategories(models.Model):
    categories = models.CharField(max_length=32, verbose_name="大类")
    image = models.CharField(max_length=64, verbose_name="图片名称")
    redirect = models.CharField(max_length=64, verbose_name="重定向目标")
    group = models.CharField(max_length=64, verbose_name="组",
                             choices=(('ventilation', '浴室暖房换气设备'), ('aeration', '新风通风设备')))

    class Meta:
        verbose_name_plural = "乐奇电器大类"

    def __unicode__(self):
        return self.categories


class Equipment(models.Model):
    identification = models.CharField(max_length=32, verbose_name="型号")
    description = models.CharField(max_length=64, verbose_name="型号描述")
    name = models.CharField(max_length=64, verbose_name="名称")
    price = models.IntegerField(verbose_name="价格")
    session = models.CharField(max_length=32, verbose_name="公司", choices=(("GE", "通用电气"), ("lifegear", "台湾乐奇")))

    categories = models.ForeignKey(EquipmentCategories, verbose_name="大类", blank=True, null=True)

    class Meta:
        verbose_name_plural = "电器型号"

    def __unicode__(self):
        return self.identification
        # return u"%s %s" % (self.name, self.identification)


class VentilationSpec(models.Model):
    operation_mode = models.CharField(max_length=32, verbose_name="主操作模式")
    secondary_mode = models.CharField(max_length=16, verbose_name="二级操作模式")
    power_consumption = models.CharField(max_length=16, verbose_name="消耗电量")
    # price = models.BigIntegerField(verbose_name="价格")

    ventilation_volume = models.CharField(max_length=16, verbose_name="换气风量")
    air_volume = models.CharField(max_length=16, verbose_name="循环风量")
    noise = models.CharField(max_length=16, verbose_name="噪音")
    maximum_pressure = models.CharField(max_length=16, verbose_name="最大静压值")
    host_weight = models.CharField(max_length=16, verbose_name="主机重量")
    pipeline = models.CharField(max_length=16, verbose_name="连接管线")
    size = models.CharField(max_length=32, verbose_name="开孔尺寸/主机尺寸/安装尺寸")

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇浴室暖房换气设备规格"


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

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇新风全热空气净化机（交换机）设备规格"


class AirSpec(models.Model):
    host_size = models.CharField(max_length=16, verbose_name="主机尺寸")
    hoisting_size = models.CharField(max_length=16, verbose_name="吊装尺寸")
    # price = models.BigIntegerField(verbose_name="价格")

    air_volume = models.CharField(max_length=16, verbose_name="适用风量")
    weight = models.CharField(max_length=16, verbose_name="重量")
    pipeline = models.CharField(max_length=16, verbose_name="连接管线")

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇空气净化箱规格"


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

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇超静音换气扇规格"


class StrongSpec(Ventilator):
    opening_size = models.CharField(max_length=16, verbose_name="开孔/安装尺寸")

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇劲风换气扇规格"


class HiddenSpec(Ventilator):
    host_size = models.CharField(max_length=16, verbose_name="主机尺寸")

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇隐藏式换气扇规格"


class CircularSpec(models.Model):
    power_consumption = models.CharField(max_length=16, verbose_name="消耗功率")
    air_volume = models.CharField(max_length=16, verbose_name="风量")
    noise = models.CharField(max_length=16, verbose_name="噪音")
    installation_dimensions = models.CharField(max_length=16, verbose_name="安装尺寸")
    applicable_area = models.CharField(max_length=16, verbose_name="适用面积")
    weight = models.CharField(max_length=16, verbose_name="重量")

    equipment = models.ManyToManyField(Equipment, verbose_name='型号')

    class Meta:
        verbose_name_plural = "乐奇节能循环扇规格"


class Agent(models.Model):
    name = models.CharField(max_length=128, verbose_name="代理商")
    phone = models.CharField(max_length=32, verbose_name="代理商电话")
    wechat = models.CharField(max_length=64, verbose_name="代理商微信", blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "合作伙伴"


class MaintenanceAuxiliary(models.Model):
    uuid = models.UUIDField(max_length=32, verbose_name="申请编号")
    equipment = models.ForeignKey(Equipment, verbose_name='型号')
    number = models.BigIntegerField(verbose_name='数量')

    def __unicode__(self):
        return u"设备型号：%s => 数量：%s" % (self.equipment, self.number)

    class Meta:
        verbose_name_plural = "维保设备及数量"


class Maintenance(models.Model):
    name = models.CharField(max_length=128, verbose_name="姓名")
    phone = models.CharField(max_length=32, verbose_name="电话")
    fix_address = models.CharField(max_length=32, verbose_name="安装地址")
    fix_date = models.DateField(verbose_name="安装日期")
    apply_time = models.DateTimeField(verbose_name="申请时间")
    uuid = models.UUIDField(max_length=32, verbose_name="申请编号")
    auxiliary = models.ManyToManyField(MaintenanceAuxiliary, verbose_name="设备及数量")
    handled = models.CharField(max_length=8, verbose_name="是否处理", choices=(("yes", "已处理"), ("no", "未处理")))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "官方维保"


class OrderAuxiliary(models.Model):
    uuid = models.UUIDField(max_length=32, verbose_name="申请编号")
    equipment = models.ForeignKey(Equipment, verbose_name='型号')
    number = models.BigIntegerField(verbose_name='数量')

    def __unicode__(self):
        return u"设备型号：%s => 数量：%s" % (self.equipment, self.number)

    class Meta:
        verbose_name_plural = "订单设备及数量"


class Order(models.Model):
    agent = models.ForeignKey(Agent, verbose_name="合作伙伴")
    receipt_address = models.CharField(max_length=128, verbose_name="收货地址")
    receipt_date = models.DateField(verbose_name="收货时间")
    order_time = models.DateTimeField(verbose_name="下单时间")
    uuid = models.UUIDField(max_length=32, verbose_name="订单编号")
    payed = models.CharField(max_length=8, verbose_name="支付", choices=(('yes', '已支付'), ('no', '未支付')))
    shipped = models.CharField(max_length=16, verbose_name="是否发货", choices=(('yes', '已发货'), ('no', '未发货')))
    valid = models.CharField(max_length=16, verbose_name="订单是否有效", choices=(('valid', '有效'), ('invalid', '无效')))

    auxiliary = models.ManyToManyField(OrderAuxiliary, verbose_name="设备及数量")

    def __unicode__(self):
        return self.agent.name

    class Meta:
        verbose_name_plural = "订单"