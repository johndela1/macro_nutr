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
	fmt.Println(foods)
}
