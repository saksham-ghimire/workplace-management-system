package grpcmanager

import (
	"client/grpcRouter"
	"client/handler"
	"context"
)

func (s *RouterServer) FetchMetaData(ctx context.Context, req *grpcRouter.MetaDataRequest) (*grpcRouter.MetaDataResponse, error) {
	switch req.GetRequestType() {
	case "system":

		systemInfo, err := handler.FetchSystemInfo()
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode: 200,
			Sysinfo:    systemInfo,
		}, nil

	case "services":

		servicesInfo, err := handler.FetchAvailableServices()
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode: 200,
			Services:   servicesInfo,
		}, nil

	case "software":
		installedSoftwares, err := handler.FetchInstalledSoftwares()
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode:         200,
			InstalledSoftwares: installedSoftwares,
		}, nil

	case "runningProcesses":
		runningProcesses, err := handler.FetchRunningProcesses()
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode:       200,
			RunningProcesses: runningProcesses,
		}, nil

	case "processesInfo":
		infoProcesses, err := handler.FetchProcessesInfo(req.GetRequestValue())
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode:    200,
			ProcessesInfo: infoProcesses,
		}, nil

	case "sysHealth":
		sysHealth, err := handler.FetchSystemHealth()
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode: 200,
			SysHealth:  sysHealth,
		}, nil

	case "network":
		netIO, err := handler.FetchNetworkIO()
		if err != nil {
			return &grpcRouter.MetaDataResponse{
				StatusCode:   500,
				ErrorMessage: err.Error(),
			}, nil
		}
		return &grpcRouter.MetaDataResponse{
			StatusCode: 200,
			NetInfo:    netIO,
		}, nil

	default:
		return &grpcRouter.MetaDataResponse{
			ErrorMessage: "unsupported meta data request type",
		}, nil
	}

}
