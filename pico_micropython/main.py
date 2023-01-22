import machine
from time import sleep
from module.helper import *
from module.wifi import *
from module.mqtt import *
from module.cradel.global_var import Flag
import config


class Main:
    def main():
        # WIFI Connection
        wifi = Wifi()
        try:
            wifi.connect()
        except KeyboardInterrupt:
            machine.reset()

        # MQTT Connect
        mqtt = Mqtt()
        mqtt.connectMQTT()
        mqtt_id = mqtt.id.decode("utf-8")
        print(f'Client id: {mqtt_id}')

        # Notify server of connection
        mqtt.publish('user/connected', str(mqtt.id.decode("utf-8")))

        temp = Temperature()

        log = Log()

        try:

            # Subscribe to toggle of lamp for user
            mqtt.test_call()
            mqtt.subscribe(f"users/{mqtt_id}/lamp/toggle")

            # Main loop
            while True:

                # look for subscribed msg
                mqtt.client.check_msg()

                # Check if new log is needed
                if log.logComp(log.getTimestampFromLog(), 60):
                    temperature = str(temp.read())

                    # publish as MQTT payload
                    mqtt.publish('picow/temperature', str(temperature))
                    log.logTemperature()
                sleep(1)
        finally:
            # Disconnect before exit
            mqtt.client.disconnect()


# Start point
if __name__ == '__main__':
    Main.main()
