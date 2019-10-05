#!/usr/bin/env python3

"""sources
https://fdc.nal.usda.gov/
https://www.calorieking.com/us/en/
https://nutritiondata.self.com/
https://www.nutritionvalue.org/
"""

import sys


class Food:
    def __init__(self, weight_g):
        self.weight_g = weight_g
        self.energy_kc = weight_g * self.energy_kc_per_g
        self.fat_g = weight_g * self.fat_g_per_g
        self.protein_g = weight_g * self.protein_g_per_g

    def __repr__(self):
        return ', '.join((
            self.__class__.__name__,
            f'grams {self.weight_g:.1f}',
            f'calories {self.energy_kc:.1f}',
            f'fat {self.fat_g:.1f}',
            f'protein {self.protein_g:.1f}',
        ))


class Meat(Food):
    energy_kc_per_g = None
    fat_g_per_g = None
    protein_g_per_g = None

    def __init__(self, weight_g, fat_prop):
        self.fat_g_per_g = fat_prop * .98
        self.protein_g_per_g = (1-fat_prop) * .23
        self.energy_kc_per_g = self.fat_g_per_g*9 + self.protein_g_per_g*4
        super().__init__(weight_g)

    @classmethod
    def from_protein_g(cls, protein_g, fat_prop):
        protein_g_per_g = cls(1, fat_prop).protein_g_per_g
        return cls(protein_g / protein_g_per_g, fat_prop)


class Liver(Food):
    energy_kc_per_g = 1.35
    fat_g_per_g = .036
    protein_g_per_g = .204


class Suet(Food):
    energy_kc_per_g = 8.54
    fat_g_per_g = .946
    protein_g_per_g = .018


def meal(energy_kc, protein_g, meat_fat_prop, liver_g):
    liver = Liver(liver_g)
    meat = Meat.from_protein_g(protein_g-liver.protein_g, meat_fat_prop)
    suet = Suet(
        (energy_kc - (liver.energy_kc + meat.energy_kc))
        / Suet.energy_kc_per_g)
    return liver, meat, suet


def fat_prop_meal(energy_kc, fat_ratio, meat_fat_prop, liver_g):
    protein_g = energy_kc/(fat_ratio*9 + 4)
    return meal(energy_kc, protein_g, meat_fat_prop, liver_g)


def fat_prop(meal):
    fat_g = sum(i.fat_g for i in meal)
    protein_g= sum(i.protein_g for i in meal)
    return fat_g / protein_g

def two_meats_meal(energy_kc):
    meat1 = Meat.from_protein_g(25, .5)
    meat2 = Meat.from_protein_g(65-25, .2)
    suet = Suet((energy_kc - (meat1.energy_kc + meat2.energy_kc)) / Suet.energy_kc_per_g)
    meal = (meat1, meat2, suet)
    for i in meal: print(i)
    print(fat_prop(meal))
    exit();


if __name__ == '__main__':
    #two_meats_meal(1900)
    if len(sys.argv) > 1:
        fat_prop = int(sys.argv[1]) / 100
        meat = Meat(1, fat_prop)
        print(meat.fat_g/meat.protein_g)
        exit()
    liver_g_per_w = 454
    liver_g_per_d = liver_g_per_w / 7
    m =  meal(energy_kc=1900, protein_g=64, meat_fat_prop=.2, liver_g=liver_g_per_d)
    for i in m:
        print(i)
    print('fat/protein ', fat_prop(m))

    # m =  fat_prop_meal(energy_kc=1900, fat_ratio=2, meat_fat_prop=.2, liver_g=liver_g_per_d)
    # for i in m:
    #     print(i)
    # print('fat/protein ', fat_prop(m))
