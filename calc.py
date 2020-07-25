#!/usr/bin/env python3


class Food:
    fat_g_per_g = 0
    protein_g_per_g = 0

    def __init__(self, weight_g):
        self.fat_g = self.fat_g_per_g * weight_g
        self.protein_g = self.protein_g_per_g * weight_g
        self.weight_g = weight_g

    @classmethod
    def from_protein_g(cls, protein_g):
        return cls(protein_g / cls.protein_g_per_g)

    def __repr__(self):
        return ", ".join(
            (
                self.__class__.__name__,
                f"grams {self.weight_g:.1f}",
                f"fat {self.fat_g:.1f}",
                f"protein {self.protein_g:.1f}",
            )
        )


class Fat(Food):
    fat_g_per_g = 0.946
    protein_g_per_g = 0.018


class Offal(Food):
    pass


class Brain(Offal):
    fat_g_per_g = 0.1
    protein_g_per_g = 0.1


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
            fat_g_per_g=fat_decimal * 0.95,
            protein_g_per_g=lean_decimal * 0.24,
        ),
    )


def fat_prop(meal):
    return sum(food.fat_g for food in meal) / sum(
        food.protein_g for food in meal
    )


if __name__ == "__main__":
    total_weight_g = 555
    protein_g = 85
    avail_meats = [
        create_meat_class(22),
    ]
    offals = [
        Liver(64),
        Tendon(0),
        Spleen(0),
        SweetBread(0),
        Brain(0),
    ]

    protein_g_per_meat = (
        protein_g - sum(offal.protein_g for offal in offals)
    ) / len(avail_meats)

    meats = [Meat.from_protein_g(protein_g_per_meat) for Meat in avail_meats]

    fats = [
        Fat(
            total_weight_g
            - (
                sum(offal.weight_g for offal in offals)
                + sum(meat.weight_g for meat in meats)
            )
        )
    ]

    foods = fats + meats + offals

    for food in foods:
        if food.weight_g:
            print(food)
    print("fat/protein ", fat_prop(foods))
    # print(
    #    sum(food.fat_g for food in foods),
    #    sum(food.protein_g for food in foods),
    # )
    print(
        sum(
            [
                sum(food.fat_g * 9 for food in foods),
                sum(food.protein_g * 4 for food in foods),
            ]
        )
    )
