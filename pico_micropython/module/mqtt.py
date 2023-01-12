from lib.umqtt.simple import MQTTClient
import ubinascii
import json
from module.helper import Lamp, MatchTopic
import machine
import config
# s = json.dumps(variables)
# variables2 = json.loads(s)
# assert variables == variables2

# print(json.dumps(variables).encode('utf-8'))
id = 'raspberrypi_picow'


class Mqtt:
    def __init__(self) -> None:
        self.id = ubinascii.hexlify(machine.unique_id())
        pass

    def connectMQTT(self) -> None:
        client = MQTTClient(client_id=self.id,
                            # client_id=b'{id}',
                            server=config.MQTT_SERVER,
                            port=1883,
                            user=config.MQTT_U,
                            password=config.MQTT_U,
                            keepalive=7200,
                            # ssl=True,
                            # ssl_params={'server_hostname':'8fbadaf843514ef286a2ae29e80b15a0.s1.eu.hivemq.cloud'}
                            )

        client.connect()
        self.client = client
        # return client

    def publish(self, topic: str, value):
        # print(topic)
        # print(value)
        self.client.publish(topic, value)
        print("publish Done")

    def subscribe(self, topic: str) -> None:
        self.client.subscribe(topic)

    def call(self, topic, msg) -> None:
        decoded_topic = topic.decode("utf-8")
        decoded_msg = msg.decode("utf-8")
        try:
            decoded_msg = json.loads(decoded_msg)
        except:
            # decoded_msg = decoded_msg
            pass
        # Matching the incoming topic
        print(MatchTopic().test(decoded_topic,
              r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+"))
        if x := MatchTopic().test(decoded_topic, r"users/[A-Za-z0-9]+/lamp/[a-zA-Z]+"):
            if x[1] == self.id.decode("utf-8"):
                Lamp().toggle()
        else:
            print('No matching topic')

    def test_call(self) -> None:
        self.client.set_callback(self.call)

    def json_to_bytes(self, data={
        "test": "test",
        "num": 12
    }):
        return
