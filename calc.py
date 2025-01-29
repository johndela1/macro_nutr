#!/usr/bin/env python3


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
        return f"{self.__class__.__name__.lower()} {self.weight_g:.1f} g"


class Suet(Food):
    fat_g_per_g = 0.946
    protein_g_per_g = 0.018


def create_meat(lean_decimal, name):
    if not (0 <= lean_decimal <= 1):
        raise ValueError("lean_decimal must be between 0 and 1")
    fat_decimal = 1 - lean_decimal
    return type(
        name,
        (Food,),
        dict(
            fat_g_per_g=fat_decimal * 0.98, protein_g_per_g=lean_decimal * 0.22
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


if __name__ == "__main__":
    Ribeye = create_meat(lean_decimal=0.80, name="ribeye")
    Lamb = create_meat(lean_decimal=0.88, name="lamb")
    Chuck = create_meat(lean_decimal=0.87, name="chuck")
    Ground75 = create_meat(lean_decimal=0.75, name="ground75")
    Ground55 = create_meat(0.55, "ground55")

    fat_g = 235
    protein_g = 80
    meals_per_day = 2

    meat1 = Chuck(0)
    meat2 = Ground75.from_protein_g(protein_g - meat1.protein_g)
    fat = Suet((fat_g - meat1.fat_g - meat2.fat_g) / Suet.fat_g_per_g)

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
