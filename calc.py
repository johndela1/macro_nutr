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
    def __init__(self, weight_g=0):
        self.energy_kc_per_g = (
            self.carb_g_per_g*4 + self.fat_g_per_g*9 + self.protein_g_per_g*4)
        self.weight_g = weight_g

    @property
    def weight_g(self):
        return self._weight_g

    @weight_g.setter
    def weight_g(self, value):
        self._weight_g = value
        self._energy_kc = self.energy_kc_per_g * value
        self.carb_g = self.carb_g_per_g * value
        self.fat_g = self.fat_g_per_g * value
        self._protein_g = self.protein_g_per_g * value

    @property
    def protein_g(self):
        return self._protein_g

    @protein_g.setter
    def protein_g(self, value):
        self._protein_g = value
        self._weight_g = value / self.protein_g_per_g
        self._energy_kc = self.energy_kc_per_g * self._weight_g
        self.carb_g = self.carb_g_per_g * self._weight_g
        self.fat_g = self.fat_g_per_g * self._weight_g

    @property
    def energy_kc(self):
        return self._energy_kc

    @energy_kc.setter
    def energy_kc(self, value):
        self._energy_kc = value
        self._weight_g = value / self.energy_kc_per_g
        self._protein = self.protein_g_per_g * self._weight_g
        self.carb_g = self.carb_g_per_g * self._weight_g
        self.fat_g = self.fat_g_per_g * self._weight_g

    def __repr__(self):
        return ', '.join((
            self.__class__.__name__,
            f'grams {self.weight_g:.1f}',
            f'calories {self.energy_kc:.1f}',
            f'fat {self.fat_g:.1f}',
            f'protein {self.protein_g:.1f}',
        ))


class Fat(Food):
    fat_g_per_g = .946
    protein_g_per_g = .018


class Meat(Food):
    pass


class Organ(Food):
    pass


class Brain(Organ):
    fat_g_per_g = .1
    protein_g_per_g = .1


class Kidney(Organ):
    carb_g_per_g = .03
    fat_g_per_g = .031
    protein_g_per_g = .174


class Spleen(Organ):
    fat_g_per_g = .03
    protein_g_per_g = .18


class SweetBread(Organ):
    fat_g_per_g = .204
    protein_g_per_g = .122


class Liver(Organ):
    carb_g_per_g = .039
    fat_g_per_g = .036
    protein_g_per_g = .204


class GB45(Meat):
    fat_g_per_g = .4
    protein_g_per_g = .14


class Primal(Meat):
    fat_g_per_g = .05
    protein_g_per_g = .25


class GB10(Meat):
    fat_g_per_g = .1
    protein_g_per_g = .2


class GB20(Meat):
    fat_g_per_g = .2
    protein_g_per_g = .172


class GB5(Meat):
    fat_g_per_g = .05
    protein_g_per_g = .214


class Ribeye(Meat):
    fat_g_per_g = .2
    protein_g_per_g = .22


class Egg(Meat):
    carb_g_per_g = .032
    fat_g_per_g = .099
    protein_g_per_g = .126


def fat_prop(meal):
    return (sum(food.fat_g for food in meal)
            / sum(food.protein_g for food in meal))


def by_type(foods, type_):
    return [food for food in foods if isinstance(food, type_)]


if __name__ == '__main__':
    energy_kc = 1900
    protein_g = 70
    organ_g = 454 / 7
    foods = (
        Fat(),
        Primal(),
        Liver(),
        Brain(),
    )

    fat = by_type(foods, Fat)[0]
    meats = by_type(foods, Meat)
    organs = by_type(foods, Organ)

    g_per_organ = organ_g / len(organs)
    for organ in organs:
        organ.protein_g = organ.protein_g_per_g * g_per_organ

    protein_g_per_meat = (protein_g - sum(organ.protein_g for organ in organs)) / len(meats)
    for meat in meats:
        meat.protein_g = protein_g_per_meat

    fat.energy_kc = (energy_kc
                    - (sum(organ.energy_kc for organ in organs)
                       + sum(meat.energy_kc for meat in meats)))

    for food in foods:
        if not food.energy_kc:
            continue
        print(food)
    print('fat/protein ', fat_prop(foods))
