# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=16, verbose_name="省名")
    e_name = models.CharField(max_length=32, verbose_name="英文名", blank=True)

    class Meta:
        verbose_name_plural = "省"

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=16, verbose_name="市名")
    e_name = models.CharField(max_length=32, verbose_name="英文名", blank=True)

    province = models.ForeignKey(Province, verbose_name="所属省")

    class Meta:
        verbose_name_plural = "市"

    def __unicode__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=16, verbose_name="区名/县名")
    e_name = models.CharField(max_length=32, verbose_name="英文名", blank=True)

    city = models.ForeignKey(City, verbose_name="所属市")

    class Meta:
        verbose_name_plural = "区/县"

    def __unicode__(self):
        return self.name