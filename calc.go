package main

import "fmt"

type food struct {
	typ          string
	fatGperG     float64
	proteinGperG float64
	weightG      float64
	fatG         float64
	proteinG     float64
}

func (f food) String() string {
	return fmt.Sprintf("%s: %.1f g", f.typ, f.weightG)
}

func NewFood(typ string, weightG, fatGperG, proteinGperG float64) food {
	f := food{}
	f.typ = typ
	f.fatGperG = fatGperG
	f.proteinGperG = proteinGperG
	f.weightG = weightG
	f.fatG = f.fatGperG * weightG
	f.proteinG = f.proteinGperG * weightG
	return f

}

func NewFat(weightG float64) food {
	fatGperG := .946
	proteinGperG := .01
	return NewFood("fat", weightG, fatGperG, proteinGperG)
}

func NewLiver(weightG float64) food {
	fatGperG := .036
	proteinGperG := .204
	return NewFood("liver", weightG, fatGperG, proteinGperG)
}

func NewBrain(weightG float64) food {
	fatGperG := .1
	proteinGperG := .1
	return NewFood("brain", weightG, fatGperG, proteinGperG)
}

func NewMeatFromProteinG(proteinG float64, fatDecimal float64) food {
	leanDecimal := 1 - fatDecimal
	fatGperG := fatDecimal * .98
	proteinGperG := leanDecimal * .21
	return NewFood("meat", proteinG/proteinGperG, fatGperG, proteinGperG)
}

func fatTotal(foods []food) float64 {
	var sum float64
	for _, f := range foods {
		sum += f.fatG
	}
	return sum
}

func proteinTotal(foods []food) float64 {
	var sum float64
	for _, f := range foods {
		sum += f.proteinG
	}
	return sum
}

func fatProp(foods []food) float64 {
	var fatSum, proteinSum float64
	for _, f := range foods {
		fatSum += f.fatG
		proteinSum += f.proteinG
	}
	return fatSum / proteinSum
}

func energyTotal(foods []food) float64 {
	var sum float64
	for _, f := range foods {
		sum += f.fatG*9 + f.proteinG*4
	}
	return sum
}

func main() {
	mealsPerDay := 2.0
	beefFatDecimal := .25
	offal := NewLiver(0)
	offal2 := NewBrain(50)
	fatG := 270.0
	proteinG := 75.0

	meat := NewMeatFromProteinG(
		proteinG-offal.proteinG-offal2.proteinG, beefFatDecimal)
	fat := NewFat(
		(fatG - offal.fatG - offal2.fatG - meat.fatG) / NewFat(0).fatGperG)
	foods := []food{fat, meat, offal, offal2}

	for i := 0; i < len(foods); i++ {
		p := &foods[i]
		p.weightG /= mealsPerDay
		p.fatG /= mealsPerDay
		p.proteinG /= mealsPerDay
	}

	for _, food := range foods {
		fmt.Println(food)
	}
	fmt.Println()

	fmt.Printf("total fat %.1f\n", fatTotal(foods))
	fmt.Printf("total protein %.1f\n", proteinTotal(foods))
	fmt.Printf("fat/protein %.1f\n", fatProp(foods))
	fmt.Printf("energy %.1f\n", energyTotal(foods))
}
