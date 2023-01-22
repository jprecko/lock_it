from lib.umqtt.simple import MQTTClient
import ubinascii
import json
from module.helper import Lamp, MatchTopic
import machine
import config
id = 'raspberrypi_picow'


class Mqtt:
    def __init__(self) -> None:
        self.id = ubinascii.hexlify(machine.unique_id())
        pass

    def connectMQTT(self) -> None:
        print(config.MQTT_SERVER)
        print(config.MQTT_U)
        print(config.MQTT_P)
        client = MQTTClient(client_id=self.id,
                            port=0,
                            server=config.MQTT_SERVER,
                            user=config.MQTT_U,
                            password=config.MQTT_P,
                            keepalive=7200)
        client.connect()
        self.client = client

    def publish(self, topic: str, value):
        self.client.publish(topic, value)
        print("publish Done")

    def subscribe(self, topic: str) -> None:
        self.client.subscribe(topic)

    # Switch for topics
    def call(self, topic, msg) -> None:
        decoded_topic = topic.decode("utf-8")
        decoded_msg = msg.decode("utf-8")
        try:
            decoded_msg = json.loads(decoded_msg)
        except:
            pass

        # Matching the incoming topic
        print(MatchTopic().test(decoded_topic,
              r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+"))
        if x := MatchTopic().test(decoded_topic, r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+"):
            if x[1] == self.id.decode("utf-8"):
                Lamp().toggle()
        else:
            print('No matching topic')
    # Set test callback

    def test_call(self) -> None:
        self.client.set_callback(self.call)
