package handler

import (
	"client/grpcRouter"

	"github.com/shirou/gopsutil/v3/net"
)

func FetchNetworkIO() (*grpcRouter.NetInformation, error) {
	netData, err := net.IOCounters(false)
	if err != nil {
		return nil, errNetwork
	}

	return &grpcRouter.NetInformation{
		InputBytes:  int32(netData[0].BytesRecv),
		OutputBytes: int32(netData[0].BytesSent),
		InputPkt:    int32(netData[0].PacketsRecv),
		OutputPkt:   int32(netData[0].PacketsSent),
	}, nil

}
