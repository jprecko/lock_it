from machine import ADC, Pin
import time
import re
import config


class Temperature:

    def __init__(self) -> None:
        self.sensor_temp = ADC(4)
        self.conversion_factor = 3.3 / (65535)
        pass

    # Read core temperature
    def read(self) -> float:
        sensor_temp = self.sensor_temp
        conversion_factor = self.conversion_factor
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706)/0.001721
        return temperature


class Csv:
    # Read CSV formated file and return a array
    def read(self, file):
        arr = []
        for x in file:
            x = x.replace('\n', '')
            arr.append(x.split(','))
        return arr

    # Write CSV format array of data to file
    def writeRow(self, file, data):
        string = ''
        for i in range(len(data)):
            if i == len(data)-1:
                string += str(data[i])+'\n'
            else:
                string += str(data[i]) + ','
        file.write(string)


class Log():

    def __init__(self) -> None:
        self.time_stamp: int
        pass

    # Write temperature to temp.csv log.
    def logTemperature(self) -> int:
        num_entries = config.NUM_LOG_ROWS | 5

        header = ['timestamp', 'temperature']
        timestamp = self.getTimestamp()

        data = [timestamp, Temperature().read()]
        csv = Csv()
        bottle_list = []
        try:
            with open('log/temp.csv', 'r+') as b:
                bottles = csv.read(b)
                bottle_list.extend(bottles)
        except:
            file = open('log/temp.csv', 'w+')
            file.close()
        with open('log/temp.csv', 'w') as b:
            csv.writeRow(b, header)
            csv.writeRow(b, data)

            for i in range(1, len(bottle_list)):
                if i > num_entries - 2:
                    break
                csv.writeRow(b, bottle_list[i])
        return timestamp

    # Get the most reascent timestamp from temp.csv log.
    def getTimestampFromLog(self) -> int | None:
        csv = Csv()
        bottle_list = []
        try:
            with open('log/temp.csv', 'r+') as b:
                bottles = csv.read(b)
                bottle_list.extend(bottles)
        except:
            return None
        try:
            return int(bottle_list[1][0])
        except:
            return None

    # Get current timestamp
    def getTimestamp(self) -> int:
        time_stamp = time.mktime(time.gmtime())
        return time_stamp

    # broken
    def getTimeFromTimestamp(self, time_stamp) -> int:
        return 1

    # Compare newest timestamp to current timestamp + secToAdd.
    def logComp(self, log, secToAdd) -> int | bool:
        time = self.getTimestamp()
        if log is None or time >= (log) + (secToAdd):
            return True
        else:
            return False


class Lamp:

    def toggle(self):
        print('toggle Led')
        led = Pin("LED", Pin.OUT)
        led.toggle()


# Look if topic is included in target.
class MatchTopic:
    def test(self, topic, target: str):
        try:
            return re.match(target, topic).group(0).split('/')
        except:
            return False
