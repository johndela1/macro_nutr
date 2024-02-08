package main

import "fmt"

type food struct {
	fat_g_per_g     float32
	protein_g_per_g float32
	weight_g        float32
	fat_g           float32
	protein_g       float32
}

type fat struct {
	food
}

func NewFat(weight_g float32) fat {
	f := fat{}
	f.fat_g_per_g = .946
	f.protein_g_per_g = .01
	f.weight_g = weight_g
	f.fat_g = f.fat_g_per_g * weight_g
	f.protein_g = f.protein_g_per_g * weight_g
	return f
}

func NewFatFromProteinG(protein_g float32) fat {
	f := NewFat(0)
	return NewFat(protein_g / f.protein_g_per_g)
}

func (f fat) String() string {
	return fmt.Sprintf("fat: %f g", f.weight_g)
}

type meat struct {
	food
}

func NewMeat(weight_g float32, fat_percent float32) meat {
	fat_decimal := fat_percent / 100
	lean_decimal := 1 - fat_decimal
	m := meat{}
	m.fat_g_per_g = fat_decimal * .98
	m.protein_g_per_g = lean_decimal * .21
	m.weight_g = weight_g
	m.fat_g = m.fat_g_per_g * weight_g
	m.protein_g = m.protein_g_per_g * weight_g
	return m
}

func NewMeatFromProteinG(protein_g float32, fat_percent float32) meat {
	m := NewMeat(0, fat_percent)
	return NewMeat(protein_g/m.protein_g_per_g, fat_percent)
}

func (m meat) String() string {
	return fmt.Sprintf("meat: %f g", m.weight_g)
}

func main() {
	meat := NewMeatFromProteinG(100, 25)
	fat := NewFat(100)
	foods := []any{meat, fat}
	fmt.Println(foods)
}
