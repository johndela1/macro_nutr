#!/usr/bin/env python3

"""sources
https://fdc.nal.usda.gov/
https://www.calorieking.com/us/en/
https://nutritiondata.self.com/
https://www.nutritionvalue.org/
"""

import sys

class Food:
    carb_g_per_g = 0
    def __init__(self):
        self.energy_kc_per_g = self.carb_g_per_g*4 + self.fat_g_per_g*9 + self.protein_g_per_g*4
        self._weight_g = 0
        self.energy_kc = 0
        self.carb_g = 0
        self.fat_g = 0
        self.protein_g = 0

    @property
    def weight_g(self):
        return self._weight_g

    @weight_g.setter
    def weight_g(self, value):
        self._weight_g = value
        self.energy_kc = self.energy_kc_per_g * value
        self.carb_g = self.carb_g_per_g * value
        self.fat_g = self.fat_g_per_g * value
        self.protein_g = self.protein_g_per_g * value


    def __repr__(self):
        return ', '.join((
            self.__class__.__name__,
            f'grams {self.weight_g:.1f}',
            f'calories {self.energy_kc:.1f}',
            f'fat {self.fat_g:.1f}',
            f'protein {self.protein_g:.1f}',
        ))


class Fat(Food):
    pass


class Meat(Food):
    pass


class Organ(Food):
    pass


class GB45(Fat):
    fat_g_per_g = .441
    protein_g_per_g = .127


class Liver(Organ):
    carb_g_per_g = .039
    fat_g_per_g = .036
    protein_g_per_g = .204


class Ribeye(Food):
    fat_g_per_g = .221
    protein_g_per_g = .175


class Suet(Fat):
    fat_g_per_g = .946
    protein_g_per_g = .018


def meal(foods, energy_kc, protein_g, organ_g):
    fat, meat, organ = foods
    organ.weight_g = organ_g
    meat.weight_g = (protein_g - organ.protein_g) / meat.protein_g_per_g
    fat.weight_g = (energy_kc - (organ.energy_kc + meat.energy_kc)) / fat.energy_kc_per_g
    return foods


def fat_prop_meal(energy_kc, fat_ratio, meat_fat_prop, liver_g):
    protein_g = energy_kc/(fat_ratio*9 + 4)
    return meal(energy_kc, protein_g, meat_fat_prop, liver_g)


def fat_prop(meal):
    fat_g = sum(i.fat_g for i in meal)
    protein_g= sum(i.protein_g for i in meal)
    return fat_g / protein_g


if __name__ == '__main__':
    fat = Suet()
    meat = GB45()
    organ = Liver()
    foods = fat, meat, organ

    organ_g_per_w = 454
    organ_g_per_d = organ_g_per_w / 7
    m =  meal(foods, energy_kc=1900, protein_g=64, organ_g=organ_g_per_d)
    for i in m:
        print(i)
    print('fat/protein ', fat_prop(m))
