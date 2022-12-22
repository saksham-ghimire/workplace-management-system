from fastapi import APIRouter, Body
from elasticsearch.elasticsearch import Elasticsearch
from manager.workstation import WorkStation
from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .utils import FirewallRule
import time
from google.protobuf.json_format import MessageToDict


class Message(BaseModel):
    message: str


router = APIRouter()


@router.get("/workstations", response_model=List[WorkStation])
async def getRegisteredWorkstations():
    rValue = []
    for _, value in WorkStation.availableWorkstations.items():
        rValue.append(value)

    return rValue


@router.get("/workstations/{hostname}", response_model=WorkStation, responses={404: {"model": Message}})
async def getWorkstationProfile(hostname):
    response = WorkStation.availableWorkstations.get(hostname)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/network")
async def getNetworkInfo(hostname: str = None, from_time: int = int(time.time())-86400, to_time: int = int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getNetworkUsage(
        hostname=hostname, from_time=from_time, to_time=to_time)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/systeminfo/{hostname}")
async def getSystemInfo(hostname: str):
    host = WorkStation.availableWorkstations.get(hostname)
    if host == None:
        return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})
    response = host.getSystemInfo()
    if response != None:

        return MessageToDict(response)

    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/systeminfo/health/{hostname}")
async def getSystemHealthInfo(hostname: str, from_time: int = int(time.time())-1800, to_time: int = int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getSystemHealthLog(hostname=hostname,
                                                  from_time=from_time, to_time=to_time)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/softwareinfo/{hostname}")
async def getSoftwareInfo(hostname: str):
    host = WorkStation.availableWorkstations.get(hostname)
    if host == None:
        return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})
    installedsoftwares = host.getSoftwareInfo()
    if installedsoftwares == None:
        return JSONResponse(status_code=404, content={
            "message": "the requested resource doesn't exist"})
    response = []
    for software in installedsoftwares:
        response.append(MessageToDict(software))
    return response


@router.get("/servicesinfo/{hostname}")
async def getServicesInfo(hostname: str):
    host = WorkStation.availableWorkstations.get(hostname)
    if host == None:
        return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})
    services = host.getServicesInfo()
    if services == None:
        return JSONResponse(status_code=404, content={
            "message": "the requested resource doesn't exist"})
    response = []
    for service in services:
        response.append(MessageToDict(service))
    return response


@router.get("/breachedLog/{hostname}")
async def stopService(hostname: str, from_time: int = int(time.time())-86400, to_time: int = int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getBreachedLog(
        hostname=hostname, from_time=from_time, to_time=to_time)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/useractivity")
async def getUserActivity(from_time: int = int(time.time())-86400, to_time: int = int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getUserActivityLog(
        from_time=from_time, to_time=to_time)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/processruntime")
async def getProcessRuntime(hostname: str = None, from_time: int = int(time.time())-86400, to_time: int = int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getRuntimeProcessLog(
        hostname=hostname, from_time=from_time, to_time=to_time)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.get("/monitoringprocesses")
async def getMonitoringProcessLog(hostname: str = None, process: str = None, from_time: int = int(time.time())-86400, to_time: int = int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getMonitoringProcessLog(
        hostname=hostname, from_time=from_time, to_time=to_time, process=process)
    if response != None:
        return response
    return JSONResponse(status_code=404, content={"message": "the requested resource doesn't exist"})


@router.post("/stopservice/{hostname}")
async def stopService(hostname: str, service: str = Body(embed=True)):
    host = WorkStation.availableWorkstations.get(hostname)

    return JSONResponse(content={"action": host.stopRunningService(service=service)})


@router.post("/startservice/{hostname}")
async def startService(hostname: str, service: str = Body(embed=True)):
    host = WorkStation.availableWorkstations.get(hostname)

    return JSONResponse(content={"action": host.startService(service=service)})


@router.post("/addfirewallrule/{hostname}")
async def addFirewallRule(hostname: str, rule: FirewallRule = Body()):
    host = WorkStation.availableWorkstations.get(hostname)
    return JSONResponse(content={"action": host.addFirewallRule(firewallRule=rule.serialize_to_protobuf())})


@router.post("/updatefirewallrule/{hostname}")
async def updateFirewallRule(hostname: str, rule: FirewallRule = Body()):
    host = WorkStation.availableWorkstations.get(hostname)
    return JSONResponse(content={"action": host.updateFirewallRule(firewallRule=rule.serialize_to_protobuf())})


@router.post("/removefirewallrule/{hostname}")
async def removeFirewallRule(hostname: str, rule: FirewallRule = Body()):
    host = WorkStation.availableWorkstations.get(hostname)
    return JSONResponse(content={"action": host.deleteFirewallRule(firewallRule=rule.serialize_to_protobuf())})
