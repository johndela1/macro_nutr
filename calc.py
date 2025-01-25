#!/usr/bin/env python3

from statistics import mean


class Food:
    fat_g_per_g: int
    protein_g_per_g: int

    def __init__(self, weight_g):
        if type(self) is __class__:
            raise TypeError("abstract class")
        self.fat_g = self.fat_g_per_g * weight_g
        self.protein_g = self.protein_g_per_g * weight_g
        self.weight_g = weight_g

    @classmethod
    def from_protein_g(cls, protein_g):
        return cls(protein_g / cls.protein_g_per_g)

    def __str__(self):
        return f"{self.__class__.__name__} {self.weight_g:.1f} g"


class Bacon(Food):
    fat_g_per_g = 0.4
    protein_g_per_g = 0.13


class GroundPork(Food):
    fat_g_per_g = 0.27
    protein_g_per_g = 0.14


class Fat(Food):
    fat_g_per_g = 0.946
    protein_g_per_g = 0.01


class Brain(Food):
    fat_g_per_g = 0.1
    protein_g_per_g = 0.1


class Liver(Food):
    fat_g_per_g = 0.036
    protein_g_per_g = 0.204


def create_meat_class(fat_decimal, name="Ground"):
    lean_decimal = 1 - fat_decimal
    return type(
        f"{name}{int(fat_decimal*100)}",
        (Food,),
        dict(
            fat_g_per_g=fat_decimal * 0.98,
            protein_g_per_g=lean_decimal * 0.21,
        ),
    )


Ribeye = create_meat_class(fat_decimal=0.20, name="Ribeye")
Lamb = create_meat_class(fat_decimal=0.12, name="Lamb")
Chuck = create_meat_class(fat_decimal=0.13, name="Chuck")
Meat25 = create_meat_class(fat_decimal=0.25)


def fat_prop(foods):
    return sum(food.fat_g for food in foods) / sum(
        food.protein_g for food in foods
    )


def energy_total(foods):
    return sum(food.fat_g * 9 for food in foods) + sum(
        food.protein_g * 4 for food in foods
    )


def protein_total(foods):
    return sum(food.protein_g for food in foods)


def fat_total(foods):
    return sum(food.fat_g for food in foods)


def good_enough(guess, M1, M2):
    meat1 = M1(guess)
    meat2 = M2.from_protein_g(protein_g - meat1.protein_g - offal.protein_g)
    return abs(meat1.weight_g - meat2.weight_g) < 1


def improve(guess, M1, M2):
    meat1 = M1(guess)
    meat2 = M2.from_protein_g(protein_g - meat1.protein_g - offal.protein_g)
    return mean([guess, meat2.weight_g])


def guess(M1, M2):
    guess = 1
    while not good_enough(guess, M1, M2):
        guess = improve(guess, M1, M2)
    return guess


if __name__ == "__main__":
    beef_density_g_per_ml = 0.96

    fat_g = 238
    protein_g = 75
    meals_per_day = 2

    offal = Brain(0)

    meat1_cls = Chuck
    meat1 = meat1_cls(guess(meat1_cls, Meat25))
    meat2 = Meat25.from_protein_g(
        protein_g - meat1.protein_g - offal.protein_g
    )

    fat = Fat(
        (fat_g - offal.fat_g - meat1.fat_g - meat2.fat_g) / Fat.fat_g_per_g
    )

    foods = [
        f.__class__(f.weight_g / meals_per_day)
        for f in [fat, meat1, meat2, offal]
        if f.weight_g
    ]

    for food in foods:
        print(food)
    print()
    print(f"total fat {fat_total(foods):.1f}")
    print(f"total protein {protein_total(foods):.1f}")
    print(f"fat/protein {fat_prop(foods):.1f}")
    print(f"energy {energy_total(foods):.1f}")
