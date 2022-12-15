package interceptor

import (
	"context"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

func UnaryAuth() grpc.UnaryServerInterceptor {
	return func(
		ctx context.Context,
		req interface{},
		info *grpc.UnaryServerInfo,
		handler grpc.UnaryHandler,
	) (interface{}, error) {
		// log.Info().Caller().Msgf("--> unary interceptor: ", info.FullMethod)

		md, ok := metadata.FromIncomingContext(ctx)
		if !ok {
			return nil, status.Errorf(codes.Unauthenticated, "metadata is not provided")
		}

		values := md["authorization-token"]
		if len(values) == 0 {
			return nil, status.Errorf(codes.Unauthenticated, "authorization token is not provided")
		}
		accessToken := values[0]
		if accessToken != "saksham" {
			return nil, status.Errorf(codes.Unauthenticated, "invalid authorization token")
		}

		return handler(ctx, req)

	}
}

func StreamAuth() grpc.StreamServerInterceptor {
	return func(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
		md, ok := metadata.FromIncomingContext(ss.Context())
		if !ok {
			return status.Errorf(codes.Unauthenticated, "metadata is not provided")
		}

		values := md["authorization-token"]
		if len(values) == 0 {
			return status.Errorf(codes.Unauthenticated, "authorization token is not provided")
		}
		accessToken := values[0]
		if accessToken != "saksham" {
			return status.Errorf(codes.Unauthenticated, "invalid authorization token")
		}
		return handler(srv, ss)
	}
}
