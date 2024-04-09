package logger

import (
	"context"
	"fmt"
	"go.uber.org/zap"

	"github.com/go-kratos/kratos/v2/errors"
	"github.com/go-kratos/kratos/v2/middleware"
	"github.com/go-kratos/kratos/v2/transport"
)

func Server(z *zap.Logger) middleware.Middleware {
	return func(handler middleware.Handler) middleware.Handler {
		return func(ctx context.Context, req interface{}) (reply interface{}, err error) {
			var (
				code      int32
				reason    string
				kind      string
				operation string
			)

			if info, ok := transport.FromServerContext(ctx); ok {
				kind = info.Kind().String()
				operation = info.Operation()
			}
			reply, err = handler(ctx, req)
			if se := errors.FromError(err); se != nil {
				code = se.Code
				reason = se.Reason
			}

			if err != nil {
				z.Error("", Data(
					"kind", "server",
					"component", kind,
					"operation", operation,
					"args", extractArgs(req),
					"code", code,
					"reason", reason,
					"stack", err,
				)...)
			} else {
				z.Info("", Data(
					"kind", "server",
					"component", kind,
					"operation", operation,
					"args", extractArgs(req),
					"code", code,
					"reason", reason,
				)...)
			}
			return
		}
	}
}

func Client(z *zap.Logger) middleware.Middleware {
	return func(handler middleware.Handler) middleware.Handler {
		return func(ctx context.Context, req interface{}) (reply interface{}, err error) {
			var (
				code      int32
				reason    string
				kind      string
				operation string
			)
			if info, ok := transport.FromClientContext(ctx); ok {
				kind = info.Kind().String()
				operation = info.Operation()
			}
			reply, err = handler(ctx, req)
			if se := errors.FromError(err); se != nil {
				code = se.Code
				reason = se.Reason
			}

			if err != nil {
				z.Error("", Data(
					"kind", "client",
					"component", kind,
					"operation", operation,
					"args", extractArgs(req),
					"code", code,
					"reason", reason,
					"stack", err,
				)...)
			} else {
				z.Info("", Data(
					"kind", "client",
					"component", kind,
					"operation", operation,
					"args", extractArgs(req),
					"code", code,
					"reason", reason,
					"stack", err,
				)...)
			}
			return
		}
	}
}

// extractArgs returns the string of the req
func extractArgs(req interface{}) string {
	if stringer, ok := req.(fmt.Stringer); ok {
		return stringer.String()
	}
	return fmt.Sprintf("%+v", req)
}

//
//// extractError returns the string of the error
//func extractError(err error) (log.Level, string) {
//	if err != nil {
//		return log.LevelError, fmt.Sprintf("%+v", err)
//	}
//	return log.LevelInfo, ""
//}
