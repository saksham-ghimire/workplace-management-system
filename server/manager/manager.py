from .workstation import WorkStation
from elasticsearch.elasticsearch import Elasticsearch
import time
import threading
from logger import logger as log

def populator(e:WorkStation):
    print("populator started")
    n = 0
    while True:
        e.sendNotification(f'message : {n}')
        print("pushed",n)
        n += 1
        time.sleep(5)


def initializeAvailableWorkstations():
    elasticInstance = Elasticsearch.getInstance()
    workstations = elasticInstance.getRegisteredWorkstations()
    if workstations == None : 
        log.warn("unable to initialize any available workstations. Please restart after checking elasticsearch connection.") 
        return
    for workstation in workstations:
        w = WorkStation(
            hostname=workstation.get("hostname"),
            ip=workstation.get("ip"),
            mail = workstation.get("mail"),
            assignedTo= workstation.get("assignedTo"),
            addedOn= workstation.get("createdOn"),
            monitoringProcesses= workstation.get("monitoringprocesses")
        )

        t= threading.Thread(target=populator,args=(w,),daemon=True)
        t.start()

def periodicDataFetch():
    elasticInstance = Elasticsearch.getInstance()
    while True:
        workstations = WorkStation.getAvailableWorkstations()
        if workstations == None: continue
        for workstation in workstations.values():
            netInfo = workstation.getNetworkInfo()
            if netInfo != None : elasticInstance.pushNetworkLog(hostname=workstation.hostname, data=netInfo)
            runningProcesses = workstation.getRunningProcesses()
            if runningProcesses != None: elasticInstance.pushProcessRuntimeLog(hostname=workstation.hostname, data=runningProcesses)
            systemHealth = workstation.getSystemHealth()
            if systemHealth != None: elasticInstance.pushHealthLog(hostname=workstation.hostname, data=systemHealth)
            monitoringProcesses = workstation.getProcessesInfo()
            if monitoringProcesses != None: 
                elasticInstance.pushMonitoringProcessLog(hostname=workstation.hostname, data=monitoringProcesses)
                for i in monitoringProcesses:
                    if i.Name in workstation.monitoringProcesses:
                        print()
        
        time.sleep(30)
            # processesInfo = workstation.getProcessesInfo([])
            # if processesInfo != None: pass #push to elasticsearch

            
