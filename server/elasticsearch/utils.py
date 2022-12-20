from enum import Enum
from typing import Callable
import json
import datetime
import time
from typing import Any
from google.protobuf.json_format import MessageToDict
from . import queries


def data_ingestor(data: dict, hostname: str) -> dict:
    data["timestamp"] = int(time.time())
    data["hostname"] = hostname
    return data

# data should only be either protobuf structure or dictionary


def post_request_serializer(hostname: str, data: Any) -> dict:

    if type(data) != dict:
        data = MessageToDict(data)
    print(data)
    return data_ingestor(hostname=hostname, data=data)


class RegisteredIndexes(Enum):
    Workstations = "workstations"
    NetworkInfo = "networkinfo"
    RuntimeProcesses = "runtimeprocesses"
    MonitoringProcesses = "monitoringprocesses"
    SystemHealth = "systemhealth"


class SupportedQueries(Enum):
    def __init__(self, url: str, func: Callable):
        self.url = url
        self.func = func

    GetWorkstationInfo = 'https://127.0.0.1:9200/workstations/_search', queries.host_based_query
    GetRegisteredWorkstations = 'https://127.0.0.1:9200/workstations/_search', queries.query_intire_index
    GetNetworkLog = 'https://127.0.0.1:9200/networkinfo/_search', queries.host_time_based_query
    GetNetworkUsage = 'https://127.0.0.1:9200/networkinfo/_search', queries.query_user_activity
    GetRuntimeProcessLog = 'https://127.0.0.1:9200/pruntime/_search', queries.query_runtime_process
    GetUserActivityLog = 'https://127.0.0.1:9200/pruntime/_search', queries.query_user_activity
    GetMonitoringProcessLog = 'https://127.0.0.1:9200/mprocesses/_search', queries.query_monitoring_process

    PostWorkstationInfo = 'https://127.0.0.1:9200/workstations/_doc', post_request_serializer
    PostNetworkInfo = 'https://127.0.0.1:9200/networkinfo/_doc', post_request_serializer
    PostRunningProcesses = 'https://127.0.0.1:9200/pruntime/_doc', post_request_serializer
    PostSystemHealth = 'https://127.0.0.1:9200/systeminfo/_doc', post_request_serializer
    PostMonitoringProcessDetail = 'https://127.0.0.1:9200/mprocesses/_doc', post_request_serializer
