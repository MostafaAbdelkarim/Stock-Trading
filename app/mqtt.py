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

cib_high = 10
cib_low = 0

edita_high = 10
edita_low = 0

hamada_high = 10
hamada_low = 0


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("thndr-trading")
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    # print("Received message: ", topic, payload.decode(), qos, properties)
    new_stock: dict = json.loads(
        payload.decode("utf-8").replace("'", '"'))
    stock_manipulation(new_stock)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


def stock_manipulation(new_stock: dict):
    if (new_stock.get('name') == 'CIB'):
        update_CIB_price_range(new_stock)
        update_stocks_to_db(new_stock, 'CIB')
    elif (new_stock.get('name') == 'Edita'):
        update_Edita_price_range(new_stock)
        update_stocks_to_db(new_stock, 'Edita')
    elif (new_stock.get('name') == 'Hamada Inc'):
        update_Hamada_price_range(new_stock)
        update_stocks_to_db(new_stock, 'Hamada Inc')


def update_stocks_to_db(new_stock: dict, stock_name: str):
    db: Session = Session(get_engine())
    query = db.query(models.Stock).filter(models.Stock.name == stock_name)
    if query.first() == None:
        raise Exception(f'Stock with name: {stock_name} not found')
    query.update(new_stock, synchronize_session=False)
    db.commit()


def update_CIB_price_range(cib_stock: dict):
    global cib_high
    global cib_low
    price: int = cib_stock.get('price')
    if (price > cib_high):
        cib_high = price
    if (price < cib_low):
        cib_low = price


def update_Edita_price_range(edita_stock: dict):
    global edita_high
    global edita_low
    price: int = edita_stock.get('price')
    if (price > edita_high):
        edita_high = price
    if (price < edita_low):
        edita_low = price


def update_Hamada_price_range(hamada_stock: dict):
    global hamada_high
    global hamada_low
    price: int = hamada_stock.get('price')
    if (price < hamada_high):
        hamada_high = price
    if (price < hamada_low):
        hamada_low = price
