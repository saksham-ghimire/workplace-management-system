from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar
from interceptor.interceptor import header_adder_interceptor
import grpc
import time
import grpcRouter.structure_pb2_grpc as structure_pb2_grpc
import grpcRouter.structure_pb2 as structure_pb2
from queue import Queue

from threading import Thread


def create_notification_channel(q:Queue):
    print("successfully created a communication channel")
    while True:
        msg = q.get()
        yield msg



@dataclass
class WorkStation:
    hostname: str
    ip: str
    mail : str
    assignedTo: str
    addedOn: str
    monitoringProcesses : list[str]
    blockingProcesses: list[str]
    active: bool = False

    availableWorkstations:ClassVar[dict[str,WorkStation]] = {}

    def __post_init__(self) -> None:
        header = header_adder_interceptor('authorization-token', 'saksham')
        self.channel = grpc.insecure_channel(f'{self.ip}:7007')
        self.channel = grpc.intercept_channel(self.channel,header)
        # to here

        self.notificationQueue = Queue()
        self.stub = structure_pb2_grpc.RouterStub(self.channel)
        t = Thread(target=self.serializeCommunicationChannel,daemon=True)
        t.start()
        self.active = True
        WorkStation.availableWorkstations[self.hostname] = self
    
    def __getMetaData(self, request:structure_pb2.MetaDataRequest) -> structure_pb2.MetaDataResponse:
        try:
            response = self.stub.FetchMetaData(request,timeout=12)
            if response.StatusCode == 200:
                return response
            else:
                return None
        except (grpc.RpcError,grpc.FutureTimeoutError) as e:
            print("Failed to connect to client please check network connectivity",e)
            return None

    def __performMetaAction(self, request:structure_pb2.MetaActionRequest) -> structure_pb2.MetaActionResponse:
        try:
            response = self.stub.PerformMetaAction(request,timeout=8)
            if response.StatusCode == 200:
                return response
            else:
                return None
        except (grpc.RpcError,grpc.FutureTimeoutError) as e:
            print("Failed to connect to client please check network connectivity",e)
            return None
    
    def getSystemInfo(self) -> structure_pb2.SystemInformation:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="system"))
        if response != None: return response.Sysinfo
        return None
    
    def getSoftwareInfo(self) -> list[structure_pb2.Software]:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="software"))
        if response != None: return response.InstalledSoftwares
        return None
    
    def getNetworkInfo(self) -> structure_pb2.NetInformation:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="network"))
        if response != None: return response.NetInfo
        return None

    def getProcessesInfo(self) -> list[structure_pb2.Process]:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="processesInfo", RequestValue=self.monitoringProcesses))
        return response.ProcessesInfo

    def getServicesInfo(self) -> list[structure_pb2.Service]:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="services"))
        if response != None: return response.Services
        return None
    
    def getSystemHealth(self) -> structure_pb2.SystemHealth:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="sysHealth"))
        if response != None: return response.SysHealth
        return None
    
    def getRunningProcesses(self) -> list[str]:
        response = self.__getMetaData(request=structure_pb2.MetaDataRequest(RequestType="runningProcesses"))
        if response != None: return response.RunningProcesses
        return None

    

    def serializeCommunicationChannel(self):
        while True:
            try:
                self.stub.CommunicationChannel(create_notification_channel(self.notificationQueue))
                print(f"Successfully serialized communication channel for ip : {self.ip}")
            
            except Exception as e:
                self.active = False
                print("Exception in communication channel will retry in 1 min",e)
                time.sleep(30)

    @classmethod
    def getAvailableWorkstations(cls) -> list[WorkStation]:
        return WorkStation.availableWorkstations
                
    def sendNotification(self, message:str):
        self.notificationQueue.put(message)
        