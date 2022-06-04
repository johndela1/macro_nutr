#!/usr/bin/env python3


class Food:
    fat_g_per_g: int
    protein_g_per_g: int

    def __init__(self, weight_g):
        self.fat_g = self.fat_g_per_g * weight_g
        self.protein_g = self.protein_g_per_g * weight_g
        self.weight_g = weight_g

    def __new__(cls, *args, **kwargs):
        assert cls is not Food, "Cannot instantiate Food"
        return super().__new__(cls)

    @classmethod
    def from_protein_g(cls, protein_g):
        return cls(protein_g / cls.protein_g_per_g)

    def __str__(self):
        return f"{self.__class__.__name__} {self.weight_g:.1f} g"


class Fat(Food):
    fat_g_per_g = 0.946
    protein_g_per_g = 0.018


class Offal(Food):
    def __init__(self, weight_g):
        if type(self) is __class__:
            raise TypeError("abstract class")
        super().__init__(weight_g)


class Brain(Offal):
    fat_g_per_g = 0.1
    protein_g_per_g = 0.1


class Marrow(Offal):
    fat_g_per_g = 0.84
    protein_g_per_g = 0.067


class Kidney(Offal):
    fat_g_per_g = 0.031
    protein_g_per_g = 0.174


class Spleen(Offal):
    fat_g_per_g = 0.03
    protein_g_per_g = 0.18


class SweetBread(Offal):
    fat_g_per_g = 0.204
    protein_g_per_g = 0.122


class Liver(Offal):
    fat_g_per_g = 0.036
    protein_g_per_g = 0.204


class Tendon(Offal):
    fat_g_per_g = 0.05
    protein_g_per_g = 0.367


class Egg(Offal):
    fat_g_per_g = 0.099
    protein_g_per_g = 0.126


def create_meat_class(fat_percent):
    fat_decimal = fat_percent / 100
    lean_decimal = 1 - fat_decimal
    return type(
        f"Meat_{fat_percent}",
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
    return sum(
        [
            sum(food.fat_g * 9 for food in foods),
            sum(food.protein_g * 4 for food in foods),
        ]
    )


if __name__ == "__main__":
    fat_g = 200
    protein_g = 75
    offal = Liver(50)
    # 25g of brain or marrow

    meat = create_meat_class(fat_percent=25).from_protein_g(
        protein_g - offal.protein_g
    )
    fat = Fat((fat_g - offal.fat_g - meat.fat_g) / Fat.fat_g_per_g)
    foods = fat, meat, offal
    foods = [f.__class__(f.weight_g / 2) for f in foods]

    for food in foods:
        if food.weight_g:
            print(food)

    print("fat/protein ", fat_prop(foods))
    print("energy", energy_total(foods))
