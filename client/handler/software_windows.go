package handler

import (
	"client/grpcRouter"
	"client/helper"
	"client/utils"

	"github.com/rs/zerolog/log"
)

func FetchInstalledSoftwares() ([]*grpcRouter.Software, error) {

	var installedSoftwares []*grpcRouter.Software
	softwares, err := helper.InstalledSoftwareList()
	if err != nil {
		log.Warn().Caller().Msgf("on attempt to get software info received error %v", err)
		return nil, errSoftware
	}
	// format softwares
	for _, software := range softwares {
		installedSoftwares = append(installedSoftwares, &grpcRouter.Software{
			Name:            software.DisplayName,
			Version:         software.DisplayVersion,
			InstallData:     software.InstallDate.String(),
			InstallLocation: software.InstallLocation,
			Size:            utils.RoundOff(int(software.EstimatedSize)),
			Publisher:       software.Publisher,
		})
	}

	return installedSoftwares, nil
}
