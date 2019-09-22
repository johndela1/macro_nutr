#!/usr/bin/env python3

from collections import namedtuple


liver_per_w_g = 454
Food = namedtuple('Food', ('gram', 'calorie', 'fat', 'protein'))


def gb_protein_g(weight_g, protein_prop_g):
    return weight_g * protein_prop_g * .25


def gb_fat_g(weight_g, fat_prop_g):
    return weight_g * fat_prop_g * .9


def fat_to_protein(prop):
    return int(gb_fat_g(100, prop)), int(gb_protein_g(100, 1-prop))


def protein_nutr(protein_g, nutr):
    return Food(*[protein_g/nutr.protein*i for i in nutr])


def fat_nutr(fat_g, nutr):
    return Food(*[fat_g/nutr.fat*i for i in nutr])


def fat(curr_cal, needed_cal):
    return (needed_cal - curr_cal) / 9


def meal(cal, total_protein, liver_protein ):
    meat_protein = total_protein - liver_protein
    liver = protein_nutr(liver_protein, Food(1, 1.91, .053, .29))
    meat = protein_nutr(meat_protein, Food(1, 2.71, .19, .25))
    # meat = protein_nutr(meat_protein, Food(1, 4.23, .41, .12))
    suet_fat = fat(liver.calorie+meat.calorie, cal)
    suet = fat_nutr(suet_fat, Food(1, 9, 1, .01))
    return [f'{i}: {int(f.gram)}' for i, f
            in (('liver', liver), ('meat', meat), ('suet', suet))]

if __name__ == '__main__':
    for i in meal(2000, 64, liver_per_w_g/7 * .29): print(i)
