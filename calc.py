#!/usr/bin/env python3


class Food:
    def __init__(self, name, fat_g_per_g, protein_g_per_g, weight_g=0):
        self.name = name
        self.fat_g_per_g = fat_g_per_g
        self.protein_g_per_g = protein_g_per_g
        self.weight_g = weight_g

    @classmethod
    def create_meat(cls, name, lean_decimal, weight_g=0):
        if not (0 <= lean_decimal <= 1):
            raise ValueError("lean_decimal must be between 0 and 1")
        fat_decimal = 1 - lean_decimal
        return cls(
            name,
            fat_g_per_g=fat_decimal * 0.98,
            protein_g_per_g=lean_decimal * 0.22,
            weight_g=weight_g,
        )

    @property
    def fat_g(self):
        return self.fat_g_per_g * self.weight_g

    @property
    def protein_g(self):
        return self.protein_g_per_g * self.weight_g

    def __call__(self, weight_g=0):
        self.weight_g = weight_g
        return self

    def __str__(self):
        return f"{self.name} {self.weight_g:.1f} g"


class Meal:
    def __init__(
        self,
        foods,
        fat,
        target_fat_g,
        target_protein_g,
        meals_per_d,
    ):
        self.target_fat_g = target_fat_g
        self.target_protein_g = target_protein_g
        self.meals_per_d = meals_per_d
        self.foods = foods
        self.balance_protein()
        fat.weight_g = (
            target_fat_g - sum(f.fat_g for f in foods)
        ) / fat.fat_g_per_g
        foods.append(fat)
        for f in foods:
            f.weight_g /= self.meals_per_d

    def __str__(self):
        out = [
            f"total fat {self.fat_total:.1f}",
            f"total protein {self.protein_total:.1f}",
            f"fat/protein {self.fat_prop:.1f}",
            f"energy {self.energy_total:.1f}",
            "---",
        ]
        return "\n".join(out + [str(f) for f in self.foods])

    def balance_protein(self):
        guess = 0
        free_foods = [f for f in self.foods if f.weight_g == 0]
        for f in self.foods:
            if f.weight_g > 0:
                f.weight_g *= self.meals_per_d
        if len(free_foods) == 0:
            raise ValueError("no free foods")
        food_count = len(self.foods)
        while abs(err := self.target_protein_g - self.protein_total > 0.1):
            guess += err / food_count
            for f in free_foods:
                f.weight_g = guess

    @property
    def fat_prop(self):
        return sum(f.fat_g for f in self.foods) / sum(
            f.protein_g for f in self.foods
        )

    @property
    def energy_total(self):
        return sum(f.fat_g * 9 for f in self.foods) + sum(
            f.protein_g * 4 for f in self.foods
        )

    @property
    def protein_total(self):
        return sum(f.protein_g for f in self.foods)

    @property
    def fat_total(self):
        return sum(f.fat_g for f in self.foods)


if __name__ == "__main__":
    chuck = Food.create_meat("chuck", lean_decimal=0.87)
    ground55 = Food.create_meat("ground55", 0.55)
    ground75 = Food.create_meat("ground75", lean_decimal=0.75)
    lamb = Food.create_meat("lamb", lean_decimal=0.88)
    ribeye = Food.create_meat("ribeye", lean_decimal=0.80)
    salmon = Food(name="salmon", fat_g_per_g=0.11, protein_g_per_g=0.20)
    suet = Food("suet", fat_g_per_g=0.946, protein_g_per_g=0.018)

    print(Meal([chuck, ground55], suet))
