package service

import (
	"context"
	pb "pytrack-service/proto/public"
)

func (s *PublicService) CarRoute(ctx context.Context, req *pb.CarRouteRequest) (*pb.CarRouteReply, error) {
	result, err := s.queryTaxiRoute(req.TaxiId)

	if err != nil {
		s.log.Error(err.Error())
	}

	return &pb.CarRouteReply{
		TaxiId:    req.TaxiId,
		Positions: result,
	}, nil
}
