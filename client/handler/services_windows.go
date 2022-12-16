package handler

import (
	"client/grpcRouter"
	"client/helper"

	"github.com/rs/zerolog/log"
)

func FetchAvailableServices() ([]*grpcRouter.Service, error) {
	var availableServices []*grpcRouter.Service
	services, err := helper.GetServices()
	if err != nil {
		log.Warn().Caller().Msgf("on attempt to get services info received error %v", err)
		return nil, errService
	}
	for _, service := range services {
		availableServices = append(availableServices, &grpcRouter.Service{
			Name:       service.DisplayName,
			Status:     service.StatusText,
			AcceptStop: service.AcceptStop,
			SCName:     service.SCName,
		})

	}
	return availableServices, nil
}

func StopRunningService(serviceName string) error {
	return helper.StopService(serviceName)
}

func StartService(serviceName string) error {
	return helper.StartService(serviceName)
}
