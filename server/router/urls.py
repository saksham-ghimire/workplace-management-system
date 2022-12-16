from fastapi import APIRouter
from elasticsearch.elasticsearch import Elasticsearch
from manager.workstation import WorkStation
from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
from google.protobuf.json_format import MessageToDict

class Message(BaseModel):
    message : str

router = APIRouter()


@router.get("/workstations",response_model=List[WorkStation])
async def getRegisteredWorkstations():
    rValue = []
    for _, value in WorkStation.availableWorkstations.items():
        rValue.append(value)

    return rValue


@router.get("/workstations/{hostname}", response_model=WorkStation,responses={404: {"model": Message}})
async def getWorkstationProfile(hostname):
    response = WorkStation.availableWorkstations.get(hostname)
    if response != None : return response
    return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})


@router.get("/network")
async def getNetworkInfo(hostname:str = None, from_time:int = int(time.time())-86400, to_time:int=int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getNetworkLog(hostname=hostname,from_time=from_time,to_time=to_time)
    if response != None : return response
    return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})


@router.get("/systeminfo/{hostname}")
async def getSystemInfo(hostname:str):
    host = WorkStation.availableWorkstations.get(hostname)
    if host == None: return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})
    response = host.getSystemInfo()
    if response != None : return MessageToDict(response)
    return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})

@router.get("/softwareinfo/{hostname}")
async def getSoftwareInfo(hostname:str):
    host = WorkStation.availableWorkstations.get(hostname)
    if host == None: return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})
    installedsoftwares = host.getSoftwareInfo()
    if installedsoftwares == None : JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})
    response = []
    for software in installedsoftwares:
        response.append(MessageToDict(software))
    return response

@router.get("/servicesinfo/{hostname}")
async def getServicesInfo(hostname:str):
    host = WorkStation.availableWorkstations.get(hostname)
    if host == None: return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})
    installedsoftwares = host.getServicesInfo()
    if installedsoftwares == None : JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})
    response = []
    for software in installedsoftwares:
        response.append(MessageToDict(software))
    return response

@router.get("/processruntime")
async def getProcessRuntime(hostname:str = None, from_time:int = int(time.time())-86400, to_time:int=int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getRuntimeProcessLog(hostname=hostname,from_time=from_time,to_time=to_time)
    if response != None : return response
    return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})

@router.get("/monitoringprocesses")
async def getMonitoringProcessLog(hostname:str = None, process:str=None,from_time:int = int(time.time())-86400, to_time:int=int(time.time())):
    elasticInstance = Elasticsearch.getInstance()
    response = elasticInstance.getMonitoringProcessLog(hostname=hostname,from_time=from_time,to_time=to_time,process=process)
    if response != None : return response
    return JSONResponse(status_code=404, content={"message":"the requested resource doesn't exist"})


@router.post("/stopservice/{hostname}")
async def stopService(hostname:str,service:str):
     host = WorkStation.availableWorkstations.get(hostname)
     
     return JSONResponse(content={"action":host.stopRunningService(service=service)})

@router.post("/startservice/{hostname}")
async def startService(hostname:str,service:str):
     host = WorkStation.availableWorkstations.get(hostname)
     
     return JSONResponse(content={"action":host.startService(service=service)})