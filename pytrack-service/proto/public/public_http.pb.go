// Code generated by protoc-gen-go-http. DO NOT EDIT.
// versions:
// - protoc-gen-go-http v2.7.0
// - protoc             v4.25.3
// source: proto/public/public.proto

package public

import (
	context "context"
	http "github.com/go-kratos/kratos/v2/transport/http"
	binding "github.com/go-kratos/kratos/v2/transport/http/binding"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the kratos package it is being compiled against.
var _ = new(context.Context)
var _ = binding.EncodeURL

const _ = http.SupportPackageIsVersion1

const OperationPublicCarRoute = "/public.Public/CarRoute"

type PublicHTTPServer interface {
	CarRoute(context.Context, *CarRouteRequest) (*CarRouteReply, error)
}

func RegisterPublicHTTPServer(s *http.Server, srv PublicHTTPServer) {
	r := s.Route("/")
	r.GET("/api/route/taxi", _Public_CarRoute0_HTTP_Handler(srv))
}

func _Public_CarRoute0_HTTP_Handler(srv PublicHTTPServer) func(ctx http.Context) error {
	return func(ctx http.Context) error {
		var in CarRouteRequest
		if err := ctx.BindQuery(&in); err != nil {
			return err
		}
		http.SetOperation(ctx, OperationPublicCarRoute)
		h := ctx.Middleware(func(ctx context.Context, req interface{}) (interface{}, error) {
			return srv.CarRoute(ctx, req.(*CarRouteRequest))
		})
		out, err := h(ctx, &in)
		if err != nil {
			return err
		}
		reply := out.(*CarRouteReply)
		return ctx.Result(200, reply)
	}
}

type PublicHTTPClient interface {
	CarRoute(ctx context.Context, req *CarRouteRequest, opts ...http.CallOption) (rsp *CarRouteReply, err error)
}

type PublicHTTPClientImpl struct {
	cc *http.Client
}

func NewPublicHTTPClient(client *http.Client) PublicHTTPClient {
	return &PublicHTTPClientImpl{client}
}

func (c *PublicHTTPClientImpl) CarRoute(ctx context.Context, in *CarRouteRequest, opts ...http.CallOption) (*CarRouteReply, error) {
	var out CarRouteReply
	pattern := "/api/route/taxi"
	path := binding.EncodeURL(pattern, in, true)
	opts = append(opts, http.Operation(OperationPublicCarRoute))
	opts = append(opts, http.PathTemplate(pattern))
	err := c.cc.Invoke(ctx, "GET", path, nil, &out, opts...)
	if err != nil {
		return nil, err
	}
	return &out, err
}
