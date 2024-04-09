package main

import (
	"github.com/go-kratos/kratos/v2"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	"github.com/go-kratos/kratos/v2/middleware/validate"
	"github.com/go-kratos/kratos/v2/transport/grpc"
	"github.com/go-kratos/kratos/v2/transport/http"
	"pytrack-service/proto/public"
	"pytrack-service/src/app/server/service"
	"pytrack-service/src/config"
	"pytrack-service/src/database"
	"pytrack-service/src/logger"
)

var (
	log  = logger.New("server.log", false, true)
	conf = config.Read(log)
)

func main() {
	db := database.Connect(conf, log)

	s := service.NewPublicService(
		service.WithPostgresql(db),
		service.WithLogger(log),
	)

	httpSrv := http.NewServer(
		http.Address(":8000"),
		http.Middleware(
			recovery.Recovery(),
			validate.Validator(),
			logger.Server(logger.New("public.log", true, false)),
		),
	)

	grpcSrv := grpc.NewServer(
		grpc.Address(":9000"),
		grpc.Middleware(
			recovery.Recovery(),
			validate.Validator(),
			logger.Server(logger.New("public.log", true, false)),
		),
	)

	public.RegisterPublicServer(grpcSrv, s)
	public.RegisterPublicHTTPServer(httpSrv, s)

	app := kratos.New(
		kratos.Name("pytrack-service"),
		kratos.Server(
			httpSrv,
			grpcSrv,
		),
	)

	if err := app.Run(); err != nil {
		log.Fatal(err.Error())
	}
}
