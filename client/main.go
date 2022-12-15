package main

import (
	grpcmanager "client/grpcManager"
	"client/grpcRouter"
	"client/interceptor"

	"net"
	"os"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

	lis, err := net.Listen("tcp", ":7007")
	if err != nil {

		log.Fatal().Err(err).Msg("Unable to listen to tcp port")
	}

	s := grpc.NewServer(
		grpc.UnaryInterceptor(interceptor.UnaryAuth()),
		// grpc.StreamInterceptor(interceptor.StreamAuth()),
	)
	grpcRouter.RegisterRouterServer(s, &grpcmanager.RouterServer{})
	// Allows grpc services discovery
	reflection.Register(s)
	log.Info().Caller().Msgf("Server listening at %v", lis.Addr())

	if err := s.Serve(lis); err != nil {
		log.Fatal().Caller().Msgf("failed to serve got error", err)
	}
}
