package handler

import (
	"client/grpcRouter"
	"client/utils"

	"github.com/shirou/gopsutil/v3/process"
)

func FetchRunningProcesses() ([]string, error) {

	runningProcesses, err := process.Processes()
	if err != nil {
		return []string{}, errProcess
	}
	var tempHolder []string
	for _, p := range runningProcesses {
		name, err := p.Name()
		if err != nil {
			continue
		}
		if !utils.ContainsInArray(name, tempHolder) {
			tempHolder = append(tempHolder, name)
		}

	}
	return tempHolder, nil
}

func FetchProcessesInfo(processesName []string) ([]*grpcRouter.Process, error) {

	var processesInfo = []*grpcRouter.Process{}
	runningProcesses, err := process.Processes()
	if err != nil {
		return nil, errProcess
	}
	for _, process := range processesName {
		pInfo, err := fetchSpecificProcessInfo(process, runningProcesses)
		if err != nil {
			continue
		}
		processesInfo = append(processesInfo, pInfo)

	}

	return processesInfo, nil

}
func fetchSpecificProcessInfo(processName string, runningProcesses []*process.Process) (*grpcRouter.Process, error) {

	var procesInstance = &grpcRouter.Process{}
	for _, p := range runningProcesses {
		name, err := p.Name()
		if err != nil {
			continue
		}
		if name == processName {
			procesInstance.IsRunning = true
			per, err := p.CPUPercent()
			if err != nil {
				continue
			}
			mem, err := p.MemoryPercent()
			if err != nil {
				continue
			}
			thread, err := p.NumThreads()
			if err != nil {
				continue
			}
			procesInstance.CpuPercent += float32(per)
			procesInstance.MemoryPercent += float32(mem)
			procesInstance.ProcessInstance += 1
			procesInstance.ActiveThreads += thread
		}
	}
	if !procesInstance.IsRunning {
		return nil, errProcessNotRunning
	}
	procesInstance.Name = processName
	return procesInstance, nil

}
