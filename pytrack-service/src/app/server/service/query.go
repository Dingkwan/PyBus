package service

import (
	pb "pytrack-service/proto/public"
	"pytrack-service/src/database/table"
)

func (s *PublicService) queryTaxiRoute(taxiId int64) ([]*pb.CarPosition, error) {
	var (
		route  []table.Position
		result []*pb.CarPosition
	)

	if err := s.db.
		Where(&table.Position{TaxiID: taxiId}).
		Order("ts desc").
		Find(&route).Error; err != nil {
		return nil, err
	}

	for _, v := range route {
		result = append(result, &pb.CarPosition{
			Latitude:  v.Latitude,
			Longitude: v.Longitude,
			Timestamp: v.Ts,
		})
	}

	return result, nil
}
