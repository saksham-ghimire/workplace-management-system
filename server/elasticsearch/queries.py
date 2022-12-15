
def query_intire_index() -> dict:
    
 return {
  "query": {
    "match_all": {
      }
  }
}


def host_based_query(hostname:str)->dict:
   
    return{
    "query": {
        "match": {
        "hostname.keyword":hostname
        }
    }
    }

def time_based_query(from_time:int,to_time:int) -> dict:
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


def host_time_based_query(from_time:int, to_time:int, hostname:str=None) -> dict:
    if hostname == None: return time_based_query(from_time=from_time,to_time=to_time)
    body = time_based_query(from_time=from_time, to_time=to_time)
    body["query"]["bool"]["must"].append({"match": {"hostname.keyword":hostname}})
    return body



def count_agg_on_process()->dict:

  return {
    "size": 0, 
    "aggs": {
      "categories_agg":{
        "terms": {
          "field": "processName.keyword"
        }
      }
    }
    }
    

def query_runtime_process(from_time:int,to_time:int,hostname:str=None) -> dict:
    if hostname != None:
        body = host_time_based_query(hostname=hostname,from_time=from_time,to_time=to_time)
    else:
        body = time_based_query(from_time=from_time,to_time=to_time)
    
    return {**body, **count_agg_on_process()}


  