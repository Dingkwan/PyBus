package service

import (
	"go.uber.org/zap"
	"gorm.io/gorm"
	pb "pytrack-service/proto/public"
)

type PublicService struct {
	pb.UnimplementedPublicServer

	db  *gorm.DB
	log *zap.Logger
}

type Option func(s *PublicService)

func (opt Option) Apply(s *PublicService) {
	opt(s)
}

func NewPublicService(opts ...Option) *PublicService {
	publicService := &PublicService{}

	for _, o := range opts {
		o.Apply(publicService)
	}

	return publicService
}

func WithPostgresql(db *gorm.DB) Option {
	return func(s *PublicService) {
		s.db = db
	}
}

func WithLogger(log *zap.Logger) Option {
	return func(s *PublicService) {
		s.log = log
	}
}
