from django.shortcuts import render

# Create your views here.
from models import Province, City, County
import json


class China():
    def __init__(self):
        self.path = "china.json"

    def load2mysql(self):
        with open(self.path) as f:
            provinces = json.load(f)

        for province in provinces:
            # print province["name"]
            p = Province(name=province["name"])
            p.save()
            for city in province["city"]:
                # print " %s" % city["name"]
                c = City(name=city["name"], province=p)
                c.save()
                for area in city["area"]:
                    # print "  %s" % area
                    cou = County(name=area, city=c)
                    cou.save()


if __name__ == "__main__":
    China().load2mysql()
