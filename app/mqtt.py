from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
from sqlalchemy.orm import Session
from . import models
from .database import get_engine
import json

mqtt_config = MQTTConfig(
    host='vernemq',
    port=1883,
    keepalive=60,
)

mqtt = FastMQTT(
    config=mqtt_config
)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("thndr-trading")
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    # print("Received message: ", topic, payload.decode(), qos, properties)
    new_stock: dict = json.loads(
        payload.decode("utf-8").replace("'", '"'))
    if (new_stock.get('name') == 'CIB'):
        update_stocks_to_db(new_stock, 'CIB')
    elif (new_stock.get('name') == 'Edita'):
        update_stocks_to_db(new_stock, 'Edita')
    elif (new_stock.get('name') == 'Hamada Inc'):
        update_stocks_to_db(new_stock, 'Hamada Inc')


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


def update_stocks_to_db(new_stock: dict, stock_name: str):
    db: Session = Session(get_engine())
    query = db.query(models.Stock).filter(models.Stock.name == stock_name)
    if query.first() == None:
        raise Exception(f'Stock with name: {stock_name} not found')
    query.update(new_stock, synchronize_session=False)
    db.commit()
