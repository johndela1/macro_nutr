#!/usr/bin/env python3


class Food:
    def __init__(self, weight_g):
        self.weight_g = weight_g
        self.energy_c = weight_g * self.energy_c_per_g
        self.fat_g = weight_g * self.fat_g_per_g
        self.protein_g = weight_g * self.protein_g_per_g

    def __repr__(self):
        return ', '.join((
            self.__class__.__name__,
            f'grams {int(self.weight_g)}',
            f'calories {int(self.energy_c)}',
            f'fat {int(self.fat_g)}',
            f'protein {int(self.protein_g)}',
        ))


class Meat(Food):
    energy_c_per_g = None
    fat_g_per_g = None
    protein_g_per_g = None

    def __init__(self, weight_g, fat_prop):
        self.fat_g_per_g = fat_prop * .9
        self.protein_g_per_g = (1-fat_prop) * .25
        self.energy_c_per_g = self.fat_g_per_g*9 + self.protein_g_per_g*4
        super().__init__(weight_g)

class Liver(Food):
    energy_c_per_g = 1.91
    fat_g_per_g = .053
    protein_g_per_g = .29


class Suet(Food):
    energy_c_per_g = 9
    fat_g_per_g = 1
    protein_g_per_g = .01


def meal(energy_c, protein_g, liver_g):
    liver = Liver(liver_g)
    meat_protein_g = protein_g - liver.protein_g
    prop_fat=.5
    meat_protein_g_per_g = Meat(1, prop_fat).protein_g_per_g
    meat = Meat(meat_protein_g / meat_protein_g_per_g, prop_fat)
    suet = Suet(
        (energy_c - (liver.energy_c + meat.energy_c))
        / Suet.energy_c_per_g)
    return liver, meat, suet


def fat_prop(meal):
    fat_g = sum(i.fat_g for i in meal)
    protein_g= sum(i.protein_g for i in meal)
    return fat_g / protein_g

if __name__ == '__main__':
    liver_g_per_w = 454
    liver_g_per_d = liver_g_per_w / 7
    m =  meal(energy_c=2000, protein_g=64, liver_g=liver_g_per_d)
    for i in m:
        print(i)
    print('fat/protein ', fat_prop(m))
