from requests.auth import HTTPBasicAuth
import requests
import json
from requests.exceptions import Timeout, ConnectionError
from .utils import SupportedQueries, RegisteredIndexes
from logger import logger as log
import grpcRouter.structure_pb2 as structure_pb2
import json


# singleton design pattern
class Elasticsearch:

    __instance = None

    def __init__(self) -> None:
        if Elasticsearch.__instance != None:
            pass
            # log here
        else:
            self.__generic_query_parameters = {
                "headers": {"content-type": "application/json"},
                "auth": HTTPBasicAuth('elastic', 'password'),
                # remove verify parameter if you don't have ssl configured on elasticsearch
                "verify": 'C:/Users/Saksham/Desktop/Pan-Ems/certs/ca/ca.crt',
            }
        Elasticsearch.__instance = self

    @staticmethod
    def getInstance():
        if Elasticsearch.__instance == None:
            Elasticsearch()
        return Elasticsearch.__instance

    def __get(self, query) -> list:
        try:
            response = requests.get(
                **query, **self.__generic_query_parameters, timeout=8)
            if response.status_code != 200:
                log.debug(f'Elasticsearch responded with {response.content}')
                return None
            resp = json.loads(response.content)
            if resp.get("aggregations") == None:
                return [i.get("_source") for i in resp.get("hits").get("hits")]
            return resp.get("aggregations")
        except (ConnectionError, Timeout) as e:
            log.debug(
                f'Unable to perform get opertation. Received exception : {e}')
            return None

    def __post(self, query):
        try:
            response = requests.post(
                **query, **self.__generic_query_parameters, timeout=8)
            if response.status_code != 201:
                log.debug(
                    f'Elasticsearch responded with {response.content}{response.status_code}')
                return None
            return True
        except (ConnectionError, Timeout) as e:
            log.debug(
                f'Unable to perform post operation. Received exception : {e}')
            return None

    def registerNewWorkStation(self, data: dict) -> bool:
        return self.__post(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.PostWorkstationInfo, params={"data": data}))

    def getWorkstationInfo(self, hostname: str) -> dict:
        response = self.__get(query=QuerySerializer.getDesignatedQuery(
            reqType=SupportedQueries.GetWorkstationInfo, params={"hostname": hostname}))
        if response != None or len(response) != 0:
            return response[0]
        return None

    def getRegisteredWorkstations(self) -> 'list[dict]':
        response = self.__get(query=QuerySerializer.getDesignatedQuery(
            reqType=SupportedQueries.GetRegisteredWorkstations, params={}))
        if response != None:
            return response
        return None

    def getNetworkLog(self, from_time: int, to_time: int, hostname: str = None):
        return self.__get(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.GetNetworkLog, params={"from_time": from_time, "to_time": to_time, "hostname": hostname}))

    def getNetworkUsage(self, from_time: int, to_time: int):
        response = self.__get(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.GetNetworkUsage, params={
                              "from_time": from_time, "to_time": to_time}))
        if response == None:
            return None
        return response.get("categories_agg").get("buckets")
        # response = {"InputBytes": abs(float(
        #     response.get("input_bytes_sum_agg").get("value")))/1000,
        #     "OutputBytes": float(response.get("output_bytes_sum_agg").get("value"))/1000,
        #     "InputPackets": float(response.get("input_packets_sum_agg").get("value")),
        #     "OutputPackets": float(response.get("output_packets_sum_agg").get("value"))
        # }
        return response

    def getRuntimeProcessLog(self, from_time: int, to_time: int, hostname: str = None):
        response = self.__get(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.GetRuntimeProcessLog, params={
                              "from_time": from_time, "to_time": to_time, "hostname": hostname}))
        if response == None:
            return None
        return response.get("categories_agg").get("buckets")

    def getUserActivityLog(self, from_time: int, to_time: int):
        response = self.__get(query=QuerySerializer.getDesignatedQuery(
            reqType=SupportedQueries.GetUserActivityLog, params={"from_time": from_time, "to_time": to_time}))
        if response == None:
            return None
        return response.get("categories_agg").get("buckets")

    def pushNetworkLog(self, hostname: str, data: structure_pb2.NetInformation):
        return self.__post(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.PostNetworkInfo, params={"data": data, "hostname": hostname}))

    def pushHealthLog(self, hostname: str, data: structure_pb2.SystemHealth):
        return self.__post(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.PostSystemHealth, params={"data": data, "hostname": hostname}))

    def pushProcessRuntimeLog(self, hostname: str, data: 'list[str]'):
        for eachLog in data:
            self.__post(query=QuerySerializer.getDesignatedQuery(reqType=SupportedQueries.PostRunningProcesses, params={
                        "data": {"processName": eachLog}, "hostname": hostname}))

    def pushMonitoringProcessLog(self, hostname: str, data: dict):
        for eachLog in data:
            self.__post(query=QuerySerializer.getDesignatedQuery(
                reqType=SupportedQueries.PostMonitoringProcessDetail, params={"data": eachLog, "hostname": hostname}))


class QuerySerializer:
    @staticmethod
    def getDesignatedQuery(reqType: SupportedQueries, params: dict) -> dict:
        url, data = reqType.url, reqType.func(**params)
        print("here", url, data)
        return {"url": url, "data": json.dumps(data)}
