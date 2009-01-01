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
import datetime
import tz

class Food:
    def __init__(self, name):
        assert len(name) > 0
        self.name     = name
        self.time     = datetime.datetime.now(tz.LocalTimezone())
        self.quantity = 1
        self.energy   = 100
    
    def get_name(self):
        return self.name
        
    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def set_quantity(self, quantity):
        if quantity < 0: quantity = 0
        self.quantity = quantity

    def get_quantity(self):
        return self.quantity

    def set_energy(self, energy):
        if energy < 0: energy = 0
        self.energy = int(energy)

    def get_energy(self):
        return self.energy
    
    name     = property(None,         get_name)
    time     = property(set_time,     get_time)
    quantity = property(set_quantity, get_quantity)
    energy   = property(set_energy,   get_energy)

if __name__ == '__main__':
    import unittest

    class FoodTest(unittest.TestCase):
        def runTest(self):
            food = Food("test")
            assert food.get_name() == "test"
            
            time = datetime.datetime(2005, 7, 18)
            food.set_time(time)
            assert food.get_time() == time

            food.set_quantity(14)
            assert food.get_quantity() == 14

            food.set_energy(548)
            assert food.get_energy() == 548

    testcase = FoodTest()
    runner   = unittest.TextTestRunner()
    runner.run(testcase)
