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


Ribeye = create_meat_class(fat_decimal=0.15, name="Ribeye")
Lamb = create_meat_class(fat_decimal=0.15, name="Lamb")
Meat15 = create_meat_class(fat_decimal=0.15)
Meat20 = create_meat_class(fat_decimal=0.20)
Meat25 = create_meat_class(fat_decimal=0.25)
Meat45 = create_meat_class(fat_decimal=0.45)


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
    fat_g = 175
    protein_g = 75
    meals_per_day = 2

    lamb = Lamb(223)
    offal = Brain(0)
    offal2 = Liver(0)

    meat = Meat25.from_protein_g(
        protein_g - lamb.protein_g - offal.protein_g - offal2.protein_g
    )
    fat = Fat(
        (fat_g - offal.fat_g - offal2.fat_g - meat.fat_g - lamb.fat_g)
        / Fat.fat_g_per_g
    )
    foods = fat, meat, lamb, offal, offal2

    foods = [f.__class__(f.weight_g / meals_per_day) for f in foods]

    for food in foods:
        print(food)
    print()
    print(f"total fat {fat_total(foods):.1f}")
    print(f"total protein {protein_total(foods):.1f}")
    print(f"fat/protein {fat_prop(foods):.1f}")
    print(f"energy {energy_total(foods):.1f}")
