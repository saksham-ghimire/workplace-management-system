package grpcmanager

import (
	"client/grpcRouter"
	"fmt"

	"github.com/gen2brain/beeep"
)

func (s *RouterServer) CommunicationChannel(stream grpcRouter.Router_CommunicationChannelServer) error {
	fmt.Println("serialized")
	for {
		msg, err := stream.Recv()
		if err != nil {
			return err
		}

		if err := beeep.Notify(fmt.Sprintf("%v", msg.GetMessageType()), fmt.Sprintf("%v", msg.GetMessage()), "assets/information.png"); err != nil {
			fmt.Println(err)
		}
		// stream.SendAndClose(&grpcRouter.EmptyResponse{})
	}
}
