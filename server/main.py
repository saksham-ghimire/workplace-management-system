from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from router.urls import router
from manager.manager import initializeAvailableWorkstations, periodicDataFetch

app = FastAPI()

initializeAvailableWorkstations()
periodicDataFetch()
app.include_router(router)

app.mount("/static", StaticFiles(directory="templates/static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request:Request):
     return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profile")
async def getProfilePage(request:Request):
    return templates.TemplateResponse("profile_view.html",{"request":request})


