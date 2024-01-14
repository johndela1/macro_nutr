#!/usr/bin/env python3

from calc import *

if __name__ == "__main__":
    offal = Brain(25)
    meat = create_meat_class(fat_percent=45)(128)
    meat2 = create_meat_class(fat_percent=25)(128)
    fat = Fat(47)
    foods = fat, meat, meat2, offal

    for food in foods:
        print(food)
    print()
    print("total fat", fat_total(foods))
    print("total protein", protein_total(foods))
    print("fat/protein ", fat_prop(foods))
    print("energy", energy_total(foods))
