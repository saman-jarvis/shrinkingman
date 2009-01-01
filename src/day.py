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
class Day:
    def __init__(self, date):
        self.date   = date
        self.weight = 0
        self.foods  = []

    def get_date(self):
        return self.date

    def set_weight(self, weight):
        self.weight = float(weight)
        
    def get_weight(self):
        return self.weight

    def add_food(self, food):
        self.foods.append(food)
        
    def remove_food(self, food):
        i = 0
        for item in self.foods:
            if item == food:
                del self.foods[i]
                return
            i = i + 1

    def get_foods(self):
        return self.foods

    date   = property(None,       get_date)
    weight = property(set_weight, get_weight)
    foods  = property(None,       get_foods)
