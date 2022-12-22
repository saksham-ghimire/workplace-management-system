from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from router.urls import router
from manager.workstation import WorkStation
from threading import Thread
from elasticsearch.elasticsearch import Elasticsearch
from manager.manager import initializeAvailableWorkstations, periodicDataFetch

app = FastAPI()

initializeAvailableWorkstations()
t = Thread(target=periodicDataFetch, daemon=True)
t.start()
app.include_router(router)

app.mount("/static", StaticFiles(directory="templates/static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    elasticInstance = Elasticsearch.getInstance()
    cards_data = {"key_1": "Users", "value_1": len(WorkStation.availableWorkstations), "key_2": "Applications", "value_2": elasticInstance.getUniqueProcessesCount(),
                  "key_3": "Monitoring", "value_3": WorkStation.getTotalNumberOfMonitoringProcesses(), "key_4": "Restricted", "value_4": WorkStation.getTotalNumberOfRestrictedProcesses()}
    return templates.TemplateResponse("index.html", {"request": request, **cards_data})


@ app.get("/profile/{hostname}")
async def getProfilePage(request: Request, hostname: str):
    elasticInstance = Elasticsearch.getInstance()
    cards_data = {"key_1": "Users", "value_1": len(WorkStation.availableWorkstations), "key_2": "Applications", "value_2": elasticInstance.getUniqueProcessesCount(),
                  "key_3": "Monitoring", "value_3": WorkStation.getTotalNumberOfMonitoringProcesses(), "key_4": "Restricted", "value_4": WorkStation.getTotalNumberOfRestrictedProcesses()}
    workstations = WorkStation.getAvailableWorkstations()
    host = workstations.get(hostname)
    if host == None:
        return templates.TemplateResponse("204_page.html", {"request": request})

    return templates.TemplateResponse("profile_view.html", {"request": request, "hostname": hostname, "data": host, **cards_data})


@ app.get("/firewallrule/{hostname}")
async def getfRulePage(request: Request, hostname: str):
    workstations = WorkStation.getAvailableWorkstations()
    host = workstations.get(hostname)
    if host == None:
        return templates.TemplateResponse("204_page.html", {"request": request})
    return templates.TemplateResponse("firewall_rule.html", {"request": request, "hostname": hostname})
