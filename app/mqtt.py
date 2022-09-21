from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi_mqtt.config import MQTTConfig
from . import utils
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
    stock_manipulation(new_stock)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


def stock_manipulation(new_stock: dict):
    utils.update_stock_ranges(new_stock)
    utils.update_stocks_to_db(new_stock)
