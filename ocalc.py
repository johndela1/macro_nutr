#!/usr/bin/env python3


class Food:
    def __init__(self, weight_g):
        self.weight_g = weight_g
        self.energy_c = weight_g * self.energy_c_per_g
        self.fat_g = weight_g * self.fat_g_per_g
        self.protein_g = weight_g * self.protein_g_per_g

    def __repr__(self):
        return f'g{self.weight_g}, c{self.energy_c}, f{self.fat_g}, p{self.protein_g}'

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


def meal(total_energy_c, total_protein_g, liver_g_per_w):
    liver = Liver(liver_g_per_w/7)
    meat_protein_g = total_protein_g - liver.protein_g
    prop_fat=.5
    meat = Meat(meat_protein_g/Meat(1, prop_fat).protein_g_per_g, prop_fat)
    suet = Suet(
        (total_energy_c - (liver.energy_c + meat.energy_c))
        / Suet.energy_c_per_g)
    return [f'{i}: {int(f.weight_g)}' for i, f
            in (('liver', liver), ('meat', meat), ('suet', suet))]

if __name__ == '__main__':
    for i in meal(total_energy_c=2000, total_protein_g=64, liver_g_per_w=454):
        print(i)
