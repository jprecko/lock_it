import machine
import _thread
from time import sleep
from module.helper import *
from module.wifi import *
from module.mqtt import *
from module.cradel.global_var import Flag
import config


class Main:
    def main():

        wifi = Wifi(config.WIFI_U, config.WIFI_P)
        try:
            wifi.connect()
        except KeyboardInterrupt:
            machine.reset()

        mqtt = Mqtt()
        mqtt.connectMQTT()
        mqtt.publish('user/connected', str(mqtt.id.decode("utf-8")))
        mqtt_id = mqtt.id.decode("utf-8")
        print(f'Client id: {mqtt_id}')

        temp = Temperature()
        log = Log()
        try:
            mqtt.test_call()
            mqtt.subscribe(f"users/{mqtt_id}/lamp/toggle")
            while True:
                # micropython.mem_info()
                mqtt.client.check_msg()
                if log.logComp(log.getTimestampFromLog(), 60):
                    temperature = str(temp.read())
                    # publish as MQTT payload
                    mqtt.publish('picow/temperature', str(temperature))

                    log.logTemperature()
                # else:
                    # print('gammal')
                # machine.
                sleep(1)
        finally:
            mqtt.client.disconnect()


def set_up() -> None:
    global mqtt
    wifi = Wifi(config.WIFI_U, config.WIFI_P)

    try:
        wifi.connect()
    except KeyboardInterrupt:
        machine.reset()

    mqtt = Mqtt()
    mqtt.connectMQTT()

    temp = Temperature()


def core0_thread():
    global mqtt

    mqtt.test_call()
    mqtt.subscribe('picow/temperature')

    try:
        while 1:
            # micropython.mem_info()
            mqtt.client.wait_msg()
    finally:
        mqtt.client.disconnect()


def core1_thread():
    global mqtt

    temp_log = open("log/temp.csv", "w")
    temp = Temperature()

    try:
        while 1:
            # micropython.mem_info()
            temperature = str(temp.read())

            # print(temperature)

            # publish as MQTT payload
            mqtt.publish('picow/temperature', temperature)

            temp_log.write(str(temperature)+",")
            temp_log.flush()
            machine.lightleep(1000 * 100)
            # sleep(100)
    finally:
        temp_log.close()
        mqtt.client.disconnect()


# _thread.allocate_lock

# set_up()
# second_thread = _thread.start_new_thread(core1_thread, ())

# _thread.allocate_lock
if __name__ == '__main__':
    Main.main()
