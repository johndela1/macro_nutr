#!/usr/bin/env python3


class Food:
    fat_g_per_g: int
    protein_g_per_g: int

    def __init__(self, weight_g=0):
        if type(self) is __class__:
            raise TypeError("abstract class")
        self.weight_g = weight_g

    @classmethod
    def from_protein_g(cls, protein_g):
        return cls(protein_g / cls.protein_g_per_g)

    @property
    def fat_g(self):
        return self.fat_g_per_g * self.weight_g

    @property
    def protein_g(self):
        return self.protein_g_per_g * self.weight_g

    def __str__(self):
        return f"{self.__class__.__name__.lower()} {self.weight_g:.1f} g"


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


def balance_protein(foods, target_protein_g):
    guess = 0
    free_foods = [f for f in foods if f.weight_g == 0]
    if len(free_foods) == 0:
        raise ValueError("no free foods")
    while abs(err := target_protein_g - protein_total(foods)) > 0.1:
        guess += err / len(foods)
        for f in free_foods:
            f.weight_g = guess


class Suet(Food):
    fat_g_per_g = 0.946
    protein_g_per_g = 0.018


class Salmon(Food):
    fat_g_per_g = 0.11
    protein_g_per_g = 0.20


if __name__ == "__main__":
    Ribeye = create_meat(lean_decimal=0.80, name="Ribeye")
    Lamb = create_meat(lean_decimal=0.88, name="Lamb")
    Chuck = create_meat(lean_decimal=0.87, name="Chuck")
    Ground75 = create_meat(lean_decimal=0.75, name="Ground75")
    Ground55 = create_meat(0.55, "Ground55")

    fat_g = 210
    protein_g = 80
    meals_per_day = 2

    foods = [Chuck(), Ground55()]
    balance_protein(foods, protein_g)
    fat = Suet((fat_g - sum(f.fat_g for f in foods)) / Suet.fat_g_per_g)
    foods.append(fat)
    foods = [type(f)(f.weight_g / meals_per_day) for f in foods if f.weight_g]

    print(f"total fat {fat_total(foods):.1f}")
    print(f"total protein {protein_total(foods):.1f}")
    print(f"fat/protein {fat_prop(foods):.1f}")
    print(f"energy {energy_total(foods):.1f}")
    print("---")
    for food in foods:
        print(food)
