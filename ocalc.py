#!/usr/bin/env python3

def gb_protein_g(weight_g, protein_prop_g):
    return weight_g * protein_prop_g * .25


def gb_fat_g(weight_g, fat_prop_g):
    return weight_g * fat_prop_g * .9


def fat_to_protein(prop):
    return int(gb_fat_g(100, prop)), int(gb_protein_g(100, 1-prop))


class Food:
    def __init__(self, weight_g):
        self.weight_g = weight_g
        self.energy_c = weight_g * self.energy_c_per_g
        self.fat_g = weight_g * self.fat_g_per_g
        self.protein_g = weight_g * self.protein_g_per_g


class Liver(Food):
    energy_c_per_g = 1.91
    fat_g_per_g = .053
    protein_g_per_g = .29


class Meat(Food):
    energy_c_per_g = 2.71
    fat_g_per_g = .19
    protein_g_per_g = .25


class Suet(Food):
    energy_c_per_g = 9
    fat_g_per_g = 1
    protein_g_per_g = .01


def meal(total_energy_c, total_protein_g, liver_g_per_w):
    liver = Liver(liver_g_per_w/7)
    meat_protein_g = total_protein_g - liver.protein_g
    meat = Meat(meat_protein_g/Meat.protein_g_per_g)
    # meat = protein_nutr(meat_protein, Food(1, 4.23, .41, .12))
    suet = Suet(
        (total_energy_c - (liver.energy_c + meat.energy_c))
        / Suet.energy_c_per_g)
    return [f'{i}: {int(f.weight_g)}' for i, f
            in (('liver', liver), ('meat', meat), ('suet', suet))]

if __name__ == '__main__':
    for i in meal(total_energy_c=2000, total_protein_g=64, liver_g_per_w=454):
        print(i)
