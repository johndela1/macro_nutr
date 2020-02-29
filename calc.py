#!/usr/bin/env python3


class Food:
    carb_g_per_g = 0
    fat_g_per_g = 0
    protein_g_per_g = 0

    def __init__(self, weight_g):
        self.carb_g = self.carb_g_per_g * weight_g
        self.fat_g = self.fat_g_per_g * weight_g
        self.energy_kc = self.energy_kc_per_g() * weight_g
        self.protein_g = self.protein_g_per_g * weight_g
        self.weight_g = weight_g

    @classmethod
    def energy_kc_per_g(cls):
        return cls.carb_g_per_g*4 + cls.fat_g_per_g*9 + cls.protein_g_per_g*4

    @classmethod
    def from_energy_kc(cls, energy_kc):
        return cls(energy_kc/cls.energy_kc_per_g())

    @classmethod
    def from_protein_g(cls, protein_g):
        return cls(protein_g/cls.protein_g_per_g)

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


class Meat(Food):
    @classmethod
    def by_fat_percent(cls, fat_percent):
        lean_percent = 100 - fat_percent
        cls.fat_g_per_g = fat_percent * .95 / 100
        cls.protein_g_per_g = lean_percent * .24 / 100
        return cls


class Egg(Offal):
    carb_g_per_g = .032
    fat_g_per_g = .099
    protein_g_per_g = .126


def fat_prop(meal):
    return (sum(food.fat_g for food in meal)
            / sum(food.protein_g for food in meal))


if __name__ == '__main__':
    energy_kc = 1800
    # pg = energy_kc / (2*9 + 4)
    # fg = 2 * pg
    # m = Primal.from_protein_g(pg)
    # print(f"fat {fg}, meat {m.weight_g}")
    protein_g = 70
    avail_meats = [Meat.by_fat_percent(20)]
    offals = [
        Liver(64),
        Tendon(0),
        Spleen(0),
        SweetBread(0),
        Brain(0),
    ]

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
