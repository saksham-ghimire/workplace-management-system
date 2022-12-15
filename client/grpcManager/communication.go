package grpcmanager

import (
	"client/grpcRouter"
	"fmt"
)

func (s *RouterServer) CommunicationChannel(stream grpcRouter.Router_CommunicationChannelServer) error {
	fmt.Println("serialized")
	for {
		msg, err := stream.Recv()
		if err != nil {
			return err
		}
		fmt.Println(msg)
		// stream.SendAndClose(&grpcRouter.EmptyResponse{})
	}
}
