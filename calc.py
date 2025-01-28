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


class Fat(Food):
    fat_g_per_g = 0.946
    protein_g_per_g = 0.01


def create_meat_class(lean_decimal, name="ground"):
    if not (0 <= lean_decimal <= 1):
        raise ValueError("lean_decimal must be between 0 and 1")
    fat_decimal = 1 - lean_decimal
    return type(
        f"{name}{int(lean_decimal*100)}",
        (Food,),
        dict(
            fat_g_per_g=fat_decimal * 0.98,
            protein_g_per_g=lean_decimal * 0.21,
        ),
    )


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
    meat2 = M2.from_protein_g(protein_g - meat1.protein_g)
    return abs(meat1.weight_g - meat2.weight_g) < 1


def improve(guess, M1, M2):
    meat1 = M1(guess)
    meat2 = M2.from_protein_g(protein_g - meat1.protein_g)
    return mean([guess, meat2.weight_g])


def guess(M1, M2):
    guess = 1
    while not good_enough(guess, M1, M2):
        guess = improve(guess, M1, M2)
    return guess


if __name__ == "__main__":
    Ribeye = create_meat_class(lean_decimal=0.80, name="ribeye")
    Lamb = create_meat_class(lean_decimal=0.88, name="lamb")
    Chuck = create_meat_class(lean_decimal=0.87, name="chuck")
    Meat75 = create_meat_class(lean_decimal=0.75)
    Meat55 = create_meat_class(lean_decimal=0.55)
    Polluck = create_meat_class(0.90, "polluck")

    fat_g = 235
    protein_g = 80
    meals_per_day = 2

    meat1 = Polluck(0)
    meat2 = Polluck.from_protein_g(protein_g - meat1.protein_g)

    fat = Fat((fat_g - meat1.fat_g - meat2.fat_g) / Fat.fat_g_per_g)

    foods = [
        type(f)(f.weight_g / meals_per_day)
        for f in (fat, meat1, meat2)
        if f.weight_g
    ]

    for food in foods:
        print(food)
    print()
    print(f"total fat {fat_total(foods):.1f}")
    print(f"total protein {protein_total(foods):.1f}")
    print(f"fat/protein {fat_prop(foods):.1f}")
    print(f"energy {energy_total(foods):.1f}")
