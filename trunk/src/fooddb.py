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
from food             import Food
from xml.sax          import saxutils
from xml.sax          import make_parser
from xml.sax.handler  import feature_namespaces
from xml.sax.saxutils import XMLGenerator
from string           import atoi
from string           import atof
import xml.utils.iso8601
import os
import datetime
import tz


class FoodDB(saxutils.DefaultHandler):
    def __init__(self):
        self.foods = {}

    def startElement(self, name, attrs):
        self.cur_val = ""
        if name == "food":
            self.cur_food = Food("unnamed")

    def characters(self, chr):
        self.cur_val = self.cur_val + chr
    
    def endElement(self, name):
        if name == "food":
            self.foods[self.cur_food.name] = self.cur_food
            
        elif name == "name":
            self.cur_food.name = self.cur_val
            
        elif name == "energy":
            self.cur_food.energy = atoi(self.cur_val)

    def getFoods(self):
        return self.foods


class FoodDBGenerator:
    def generate(self, filename, foods):
        fp  = open(filename, "w")
        out = XMLGenerator(fp, 'utf-8')
        out.startDocument()
        out.startElement("fooddb", {})
        for food in foods:
            food = foods[food]
            out.startElement("food", {})

            out.startElement("name", {})
            out.characters(food.name)
            out.endElement("name")

            out.startElement("energy", {})
            out.characters(str(food.energy))
            out.endElement("energy")
            
            out.endElement("food")

        out.endElement("fooddb")
        out.endDocument()
        fp.close()


XML_FILE = "fooddbtest.xml"

if __name__ == '__main__':
    import unittest

    class FoodDBTest(unittest.TestCase):
        def setUp(self):
            self.parser = make_parser()
            self.parser.setFeature(feature_namespaces, 0)

        def runTest(self):
            # Generate an XML file first.
            foods = {}
            for i in range(20):
                food = Food("Testfood " + str(i))
                food.energy   = 100 * i
                foods[food.name] = food
            gen = FoodDBGenerator();
            gen.generate(XML_FILE, foods)
            
            # Now read.
            db = FoodDB()
            self.parser.setContentHandler(db)
            self.parser.parse(XML_FILE)
            assert len(db.getFoods()) == 20
            
            os.remove(XML_FILE)

    testcase = FoodDBTest()
    runner   = unittest.TextTestRunner()
    runner.run(testcase)
