package service

import (
	"context"

	pb "pytrack-service/proto/public"
)

type PublicService struct {
	pb.UnimplementedPublicServer
}

func NewPublicService() *PublicService {
	return &PublicService{}
}

func (s *PublicService) CarRoute(ctx context.Context, req *pb.CarRouteRequest) (*pb.CarRouteReply, error) {
	return &pb.CarRouteReply{}, nil
}
