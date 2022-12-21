package handler

import (
	"client/grpcRouter"
	"client/utils"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/host"
	"github.com/shirou/gopsutil/v3/mem"
)

func FetchSystemHealth() (*grpcRouter.SystemHealth, error) {
	percent, err := cpu.Percent(time.Duration(time.Second*3), false)
	if err != nil {
		return nil, errSystem
	}
	cputime, err := cpu.Times(false)
	if err != nil {
		return nil, errSystem
	}
	rinfo, err := mem.VirtualMemory()
	if err != nil {
		return nil, errSystem
	}
	temp, err := host.SensorsTemperatures()
	if err != nil {
		return nil, errSystem
	}
	var aggTemperature int
	for _, v := range temp {
		aggTemperature += int(v.Temperature)
	}
	cpuInfo := &grpcRouter.SystemHealth{
		CpuPercent:  int32(percent[0]),
		Temperature: int32(aggTemperature),
		InUseRam:    utils.RoundOff(int(rinfo.Used)),
		CpuOpSystem: int32(cputime[0].System),
		CpuOpIO:     int32(cputime[0].Iowait),
		CpuOpIdle:   int32(cputime[0].Idle),
		CpuOpUser:   int32(cputime[0].User),
	}
	return cpuInfo, nil
}
