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
    target_fat_g = 255
    target_protein_g = 85
    Ground = create_meat_class(fat_percent=45)
    Steak = create_meat_class(fat_percent=5)
    precision = 4
    for i in range(precision * (target_protein_g + 1)):
        foods = (
            Ground.from_protein_g(i / precision),
            Steak.from_protein_g(
                (target_protein_g * precision - i) / precision
            ),
        )
        if abs(target_fat_g - fat_total(foods)) > 0.5:
            continue
        print("------- begin recs -------")
        foods = [f.__class__(f.weight_g / 2) for f in foods]
        for food in foods:
            print(food)
        print("fat", fat_total(foods))
        print("protein", protein_total(foods))
        print("fat/protein ", fat_prop(foods))
        print("energy", energy_total(foods))
