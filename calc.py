#!/usr/bin/env python3


class Food:
    fat_g_per_g: int
    protein_g_per_g: int

    def __init__(self, weight_g):
        self.fat_g = self.fat_g_per_g * weight_g
        self.protein_g = self.protein_g_per_g * weight_g
        self.weight_g = weight_g

    @classmethod
    def from_protein_g(cls, protein_g):
        return cls(protein_g / cls.protein_g_per_g)

    def __str__(self):
        return f"{self.__class__.__name__} {self.weight_g:.1f}g"


class Fat(Food):
    fat_g_per_g = 0.71
    protein_g_per_g = 0.08


class Suet(Food):
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


class Liver(Offal):
    fat_g_per_g = 0.036
    protein_g_per_g = 0.204


def create_meat_class(fat_percent):
    fat_decimal = fat_percent / 100
    lean_decimal = 1 - fat_decimal
    return type(
        f"Meat{fat_percent}",
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


if __name__ == "__main__":
    ground_beef_fat = 25
    prime_rib_fat = 16
    top_sirloin_fat = 5

    protein_g = 82
    offal = Liver(0)
    fat_g = 242

    meat = create_meat_class(fat_percent=ground_beef_fat).from_protein_g(
        protein_g - offal.protein_g
    )
    fat = Fat((fat_g - offal.fat_g - meat.fat_g) / Fat.fat_g_per_g)
    foods = fat, meat, offal
    foods = [f.__class__(f.weight_g / 2) for f in foods]

    for food in foods:
        print(food)
    print()
    print("total fat", fat_total(foods))
    print("total protein", protein_total(foods))
    print("fat/protein ", fat_prop(foods))
    print("energy", energy_total(foods))
