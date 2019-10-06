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
    fat_g_per_g = .946
    protein_g_per_g = .018


class Meat(Food):
    pass


class Organ(Food):
    pass


class Brain(Organ):
    fat_g_per_g = .103
    protein_g_per_g = .109


class GB45(Meat):
    fat_g_per_g = .441
    protein_g_per_g = .127


class Liver(Organ):
    carb_g_per_g = .039
    fat_g_per_g = .036
    protein_g_per_g = .204


class Ribeye(Meat):
    fat_g_per_g = .221
    protein_g_per_g = .175


def fat_prop(meal):
    return (sum(food.fat_g for food in meal)
            / sum(food.protein_g for food in meal))


def by_type(foods, type_):
    return [f for f in foods if isinstance(f, type_)]


if __name__ == '__main__':
    energy_kc = 1900
    protein_g=64
    organ_g = 454 / 7
    foods = (
        Fat(),
        GB45(),
        Liver(organ_g),
        Ribeye(),
    )

    fat = by_type(foods, Fat)[0]
    meats = by_type(foods, Meat)
    organ = by_type(foods, Organ)[0]

    protein_g_per_meat = (protein_g - organ.protein_g) / len(meats)
    for meat in meats:
        meat.weight_g = protein_g_per_meat / meat.protein_g_per_g

    fat.weight_g = (energy_kc
                    - (organ.energy_kc + sum(meat.energy_kc for meat in meats)
                    )) / fat.energy_kc_per_g

    for food in foods:
        print(food)
    print('fat/protein ', fat_prop(foods))
