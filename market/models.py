from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Appliances(models.Model):
    identification = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.BigIntegerField()

    def __unicode__(self):
        return u"%s %s" % (self.description, self.identification)


class Agent(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    wechat = models.CharField(max_length=64)

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