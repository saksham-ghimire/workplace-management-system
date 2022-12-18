from .workstation import WorkStation
from elasticsearch.elasticsearch import Elasticsearch
import time
import grpcRouter.structure_pb2 as structure_pb2
from logger import logger as log


def initializeAvailableWorkstations():
    elasticInstance = Elasticsearch.getInstance()
    workstations = elasticInstance.getRegisteredWorkstations()
    if workstations == None:
        log.warn(
            "unable to initialize any available workstations. Please restart after checking elasticsearch connection.")
        return
    for workstation in workstations:
        w = WorkStation(
            hostname=workstation.get("hostname"),
            ip=workstation.get("ip"),
            mail=workstation.get("mail"),
            assignedTo=workstation.get("assignedTo"),
            addedOn=workstation.get("createdOn"),
            monitoringProcesses=workstation.get("monitoringprocesses"),
            restricedProcesses=workstation.get("restrictedProcesses")
        )


def periodicDataFetch():
    elasticInstance = Elasticsearch.getInstance()
    while True:
        print("fetching again")
        workstations = WorkStation.getAvailableWorkstations()
        if workstations == None:
            continue
        for workstation in workstations.values():
            netInfo = workstation.getNetworkInfo()
            if netInfo != None:
                elasticInstance.pushNetworkLog(
                    hostname=workstation.hostname, data=netInfo)
            runningProcesses = workstation.getRunningProcesses()
            if runningProcesses != None:
                elasticInstance.pushProcessRuntimeLog(
                    hostname=workstation.hostname, data=runningProcesses)
                breaches = set(workstation.restricedProcesses).intersection(
                    runningProcesses)
                if breaches != set():
                    for i in breaches:
                        req = structure_pb2.StreamRequest(
                            MessageType="Warning", Message=f'restriced application {i} has been detected running, this incident will be reported')
                        workstation.sendNotification(req)

            systemHealth = workstation.getSystemHealth()
            if systemHealth != None:
                elasticInstance.pushHealthLog(
                    hostname=workstation.hostname, data=systemHealth)
            monitoringProcesses = workstation.getProcessesInfo()
            if monitoringProcesses != None:
                elasticInstance.pushMonitoringProcessLog(
                    hostname=workstation.hostname, data=monitoringProcesses)

        time.sleep(30)
        # processesInfo = workstation.getProcessesInfo([])
        # if processesInfo != None: pass #push to elasticsearch
