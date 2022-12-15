package grpcmanager

import "client/grpcRouter"

type RouterServer struct {
	grpcRouter.UnimplementedRouterServer
}
