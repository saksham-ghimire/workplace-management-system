from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from router.urls import router
from manager.workstation import WorkStation
from threading import Thread
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
    cards_data = {"key_1": "Users", "value_1": len(WorkStation.availableWorkstations), "key_2": "Applications", "value_2": 7,
                  "key_3": "Monitoring", "value_3": WorkStation.getTotalNumberOfMonitoringProcesses(), "key_4": "Firewall", "value_4": 7}
    return templates.TemplateResponse("index.html", {"request": request, **cards_data})


@ app.get("/profile/{hostname}")
async def getProfilePage(request: Request, hostname: str):
    cards_data = {"key_1": "network", "value_1": 7, "key_2": "Applications", "value_2": 7,
                  "key_3": "Monitoring", "value_3": 7, "key_4": "breachlogs", "value_4": 7}
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
