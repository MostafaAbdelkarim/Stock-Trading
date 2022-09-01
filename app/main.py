from fastapi import FastAPI
from . import mqtt, utils
from .database import engine
from . import models
from .routers import user, stock
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
utils.initial_data_seeder()

time.sleep(5)
mqtt.mqtt.init_app(app)


@app.get("/", tags=['Home'])
def root():
    return {"Message": "Welcome to Thndr Assessment :D"}


app.include_router(user.router)
app.include_router(stock.router)
