package handler

import (
	"client/grpcRouter"
	"client/utils"
	"fmt"

	"github.com/rs/zerolog/log"
	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/host"
	"github.com/shirou/gopsutil/v3/mem"
)

func FetchSystemInfo() (*grpcRouter.SystemInformation, error) {

	var disksInfo []*grpcRouter.Disk
	var cpuInfo []*grpcRouter.Cpu

	// Get memory/RAM Info
	memStat, err := mem.VirtualMemory()
	if err != nil {
		log.Warn().Caller().Msgf("on attempt to get ram info received error %v", err)
		return nil, errSystem
	}

	// Get host Info
	hostInfo, err := host.Info()
	if err != nil {
		log.Warn().Caller().Msgf("on attempt to get host info received error %v", err)
		return nil, errSystem
	}
	// Get disk partition Info
	diskPartitions, err := disk.Partitions(false)
	if err != nil {
		log.Warn().Caller().Msgf("on attempt to get disks info received error %v", err)
		return nil, errSystem
	}

	// Get cpu info
	allCPUs, err := cpu.Info()
	if err != nil {
		log.Warn().Caller().Msgf("on attempt to get cpus info received error %v", err)
		return nil, errSystem
	}

	// format partition output
	for _, partition := range diskPartitions {
		usage, err := disk.Usage(partition.Mountpoint)
		if err != nil {
			// log here
			continue
		}
		disk := &grpcRouter.Disk{
			Name:  usage.Path,
			Total: utils.RoundOff(int(usage.Total)),
			Used:  utils.RoundOff(int(usage.Used)),
		}
		disksInfo = append(disksInfo, disk)
	}

	// format Cpu output

	for _, eachCPU := range allCPUs {
		cpu := &grpcRouter.Cpu{
			VendorId: eachCPU.VendorID,
			Model:    eachCPU.ModelName,
			Cores:    fmt.Sprintf("%v", eachCPU.Cores),
		}
		cpuInfo = append(cpuInfo, cpu)
	}

	sysInfo := &grpcRouter.SystemInformation{
		Hostname:        hostInfo.Hostname,
		Platform:        hostInfo.Platform,
		PlatformVersion: hostInfo.PlatformFamily,
		KernelVersion:   hostInfo.KernelVersion,
		KernelArch:      hostInfo.KernelArch,
		OS:              hostInfo.OS,
		TotalRAM:        utils.RoundOff(int(memStat.Total)),
		Disks:           disksInfo,
		Cpus:            cpuInfo,
	}

	return sysInfo, nil
}
