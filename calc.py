#!/usr/bin/env python3

"""sources
https://fdc.nal.usda.gov/
https://www.calorieking.com/us/en/
https://nutritiondata.self.com/
https://www.nutritionvalue.org/
"""

class Food:
    carb_g_per_g = 0
    fat_g_per_g = 0
    protein_g_per_g = 0

    def __init__(self, weight_g):
        self.weight_g = weight_g
        self.carb_g = self.carb_g_per_g * weight_g
        self.fat_g = self.fat_g_per_g * weight_g

    @classmethod
    def energy_kc_per_g(cls):
        return cls.carb_g_per_g*4 + cls.fat_g_per_g*9 + cls.protein_g_per_g*4

    @classmethod
    def from_weight_g(cls, weight_g):
        obj = cls(weight_g)
        obj.energy_kc = cls.energy_kc_per_g() * weight_g
        obj.protein_g = cls.protein_g_per_g * weight_g
        return obj

    @classmethod
    def from_energy_kc(cls, energy_kc):
        obj = cls(energy_kc / cls.energy_kc_per_g())
        obj.energy_kc = energy_kc
        obj.protein_g = cls.protein_g_per_g * obj.weight_g
        return obj

    @classmethod
    def from_protein_g(cls, protein_g):
        obj = cls(protein_g / cls.protein_g_per_g)
        obj.energy_kc = cls.energy_kc_per_g() * obj.weight_g
        obj.protein_g = protein_g
        return obj

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


class Offal(Food):
    pass


class Brain(Offal):
    fat_g_per_g = .1
    protein_g_per_g = .1


class Kidney(Offal):
    carb_g_per_g = .03
    fat_g_per_g = .031
    protein_g_per_g = .174


class Spleen(Offal):
    fat_g_per_g = .03
    protein_g_per_g = .18


class SweetBread(Offal):
    fat_g_per_g = .204
    protein_g_per_g = .122


class Liver(Offal):
    carb_g_per_g = .039
    fat_g_per_g = .036
    protein_g_per_g = .204


class Tendon(Offal):
    fat_g_per_g = .05
    protein_g_per_g = .367


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


if __name__ == '__main__':
    energy_kc = 2000
    protein_g = 70
    avail_meats = [Primal]
    offals = [Liver.from_weight_g(64), Brain.from_weight_g(0)]

    protein_g_per_meat = (
        protein_g - sum(offal.protein_g for offal in offals)
    ) / len(avail_meats)

    meats = [meat.from_protein_g(protein_g_per_meat) for meat in avail_meats]

    fat = Fat.from_energy_kc(energy_kc
                    - (sum(offal.energy_kc for offal in offals)
                       + sum(meat.energy_kc for meat in meats)))

    foods = [fat] + meats + offals

    for food in foods:
        if not food.energy_kc:
            continue
        print(food)
    print('fat/protein ', fat_prop(foods))
