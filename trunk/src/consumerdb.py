#!/usr/bin/python
##
# Author: Samuel Abels <spam debain org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##
from day  import Day
from food import Food
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax.saxutils import XMLGenerator
import xml.utils.iso8601
import os
import datetime
import tz
import unittest
from string import atoi
from string import atof


class ConsumerDB(saxutils.DefaultHandler):
    def __init__(self, from_time = None, to_time = None):
        self.search_from_time = from_time
        self.search_to_time   = to_time
        self.days             = {}

    def startElement(self, name, attrs):
        self.cur_val = ""
        if name == "day":
            date = attrs.get("date", None)
            date = xml.utils.iso8601.parse(date)
            if self.search_from_time and date < self.search_from_time: return
            if self.search_to_time   and date > self.search_to_time:   return
            date = datetime.date.fromtimestamp(date)
            self.cur_day = Day(date)
          
        elif name == "food":
            ftime = attrs.get("time", None)
            ftime = xml.utils.iso8601.parse(ftime)
            if self.search_from_time and ftime < self.search_from_time: return
            if self.search_to_time   and ftime > self.search_to_time:   return
            self.cur_food = Food(attrs.get("name", None))
            time = datetime.datetime.fromtimestamp(ftime, tz.LocalTimezone())
            self.cur_food.set_time(time)

    def characters(self, chr):
        self.cur_val = self.cur_val + chr
    
    def endElement(self, name):
        if name == "day":
            self.days[self.cur_day.date.ctime()] = self.cur_day
            
        elif name == "food":
            self.cur_day.add_food(self.cur_food)
            
        elif name == "weight":
            self.cur_day.set_weight(atoi(self.cur_val))
            
        elif name == "quantity":
            self.cur_food.quantity = atof(self.cur_val)

        elif name == "energy":
            self.cur_food.energy = atoi(self.cur_val)

    def getDays(self):
        return self.days


class ConsumerDBGenerator:
    def generate(self, filename, days):
        fp  = open(filename, "w")
        out = XMLGenerator(fp, 'utf-8')
        out.startDocument()
        out.startElement("consumerdb", {})
        for day in days:
            day  = days[day]
            time = datetime.time(0, 0, 0, 0, tz.LocalTimezone())
            date = datetime.datetime.combine(day.get_date(), time)
            date = date.isoformat()
            out.startElement("day", { "date": date })

            out.startElement("weight", {})
            out.characters(str(day.weight))
            out.endElement("weight")

            for food in day.get_foods():
                args = {
                  "name": food.name,
                  "time": food.time.isoformat()
                }
                out.startElement("food", args)
                
                out.startElement("quantity", {})
                out.characters(str(food.quantity))
                out.endElement("quantity")
                
                out.startElement("energy", {})
                out.characters(str(food.energy))
                out.endElement("energy")
                
                out.endElement("food")

            out.endElement("day")

        out.endElement("consumerdb")
        out.endDocument()
        fp.close()


XML_FILE = "consumerdbtest.xml"

class ConsumerDBTest(unittest.TestCase):
    def setUp(self):
        self.parser = make_parser()
        self.parser.setFeature(feature_namespaces, 0)

    def runTest(self):
        # Generate an XML file first.
        days = {}
        for f in range(20):
            curtime = datetime.datetime(2005, 6, f + 1, 0, 0, 0, 0, tz.LocalTimezone())
            day = Day(curtime)
            day.set_weight(100)
            for i in range(20):
                food = Food("Testfood " + str(i))
                food.quantity = 10 + i
                food.energy   = 100 * i
                food.time     = curtime
                day.add_food(food)
            days[curtime.ctime()] = day
        gen = ConsumerDBGenerator();
        gen.generate(XML_FILE, days)
        
        # Now read.
        db = ConsumerDB()
        self.parser.setContentHandler(db)
        self.parser.parse(XML_FILE)
        assert len(db.getDays()) == 20
        
        os.remove(XML_FILE)

if __name__ == '__main__':
    testcase = ConsumerDBTest()
    runner   = unittest.TextTestRunner()
    runner.run(testcase)
