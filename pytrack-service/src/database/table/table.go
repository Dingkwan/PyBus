package table

import "gorm.io/gorm"

type Position struct {
	gorm.Model
	TaxiID    int64
	Longitude float64
	Latitude  float64
	Ts        int64
}
