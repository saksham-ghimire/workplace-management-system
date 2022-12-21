
def query_intire_index() -> dict:

    return {
        "query": {
            "match_all": {
            }
        }
    }


def host_based_query(hostname: str) -> dict:

    return {
        "query": {
            "match": {
                "hostname.keyword": hostname
            }
        }
    }


def time_based_query(from_time: int, to_time: int) -> dict:
    return {

        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "timestamp": {
                                "gte": from_time,
                                "lte": to_time
                            }
                        }
                    }
                ]
            }
        }
    }


def host_time_based_query(from_time: int, to_time: int, hostname: str = None) -> dict:
    if hostname == None:
        return time_based_query(from_time=from_time, to_time=to_time)
    body = time_based_query(from_time=from_time, to_time=to_time)
    body["query"]["bool"]["must"].append(
        {"match": {"hostname.keyword": hostname}})
    return body


def count_agg_on_host(size: int) -> dict:

    return {
        "size": 0,
        "aggs": {
            "categories_agg": {
                "terms": {
                    "field": "hostname.keyword",
                    "order": {
                        "_count": "desc",
                    },
                    "size": size

                },
            }
        }
    }


def count_agg_on_process(size: int) -> dict:

    return {
        "size": 0,
        "aggs": {
            "categories_agg": {
                "terms": {
                    "field": "processName.keyword",
                    "order": {
                        "_count": "desc",
                    },
                    "size": size

                },
            }
        }
    }


def sum_agg_on_network() -> dict:
    return {
        "size": 0,
        "aggs": {
            "input_bytes_sum_agg":  {"sum": {"field": "InputBytes"}},
            "output_bytes_sum_agg":  {"sum": {"field": "OutputBytes"}},
            "input_packets_sum_agg":  {"sum": {"field": "InputPkt"}},
            "output_packets_sum_agg":  {"sum": {"field": "OutputPkt"}},

        }
    }


def query_system_health(from_time: int, to_time: int, hostname: str) -> dict:
    return {**host_time_based_query(from_time=from_time, to_time=to_time, hostname=hostname)}


def query_host_based_count(from_time: int, to_time: int) -> dict:
    return {**time_based_query(from_time=from_time, to_time=to_time), **count_agg_on_host(5)}


def query_network_usage(from_time: int, to_time: int, hostname: str) -> dict:
    if hostname != None:
        return {**host_time_based_query(from_time=from_time, to_time=to_time, hostname=hostname)}
    return {**time_based_query(from_time=from_time, to_time=to_time), **count_agg_on_host(5)}


def query_runtime_process(from_time: int, to_time: int, hostname: str = None) -> dict:
    if hostname != None:
        body = host_time_based_query(
            hostname=hostname, from_time=from_time, to_time=to_time)
    else:
        body = time_based_query(from_time=from_time, to_time=to_time)

    return {**body, **count_agg_on_process(10)}


def query_monitoring_process(from_time: int, to_time: int, hostname: str = None, process: str = None) -> dict:
    if hostname != None:
        body = host_time_based_query(
            hostname=hostname, from_time=from_time, to_time=to_time)
    else:
        body = time_based_query(from_time=from_time, to_time=to_time)

    if process != None:
        body["query"]["bool"]["must"].append(
            {"match": {"Name.keyword": process}})

    return body
