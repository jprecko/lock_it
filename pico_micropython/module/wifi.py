import network
from time import sleep
import config


class Wifi:
    def __init__(self) -> None:
        self.ssid = config.WIFI_U
        self.password = config.WIFI_P
        pass

    def connect(self) -> str:
        # Connect to WLAN
        global mqtt
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
        ip = wlan.ifconfig()[0]
        print(f'Connected on {ip}')
        return ip
