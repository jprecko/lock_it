from machine import ADC, Pin
import time
import re
import config


class Temperature:

    def __init__(self) -> None:
        self.sensor_temp = ADC(4)
        self.conversion_factor = 3.3 / (65535)
        pass

    def read(self) -> float:
        sensor_temp = self.sensor_temp
        conversion_factor = self.conversion_factor

        reading = sensor_temp.read_u16() * conversion_factor

        # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
        # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
        temperature = 27 - (reading - 0.706)/0.001721
        # print(f'{temperature}', end='\n')
        return temperature


class Csv:

    def read(self, file):
        arr = []
        for x in file:
            x = x.replace('\n', '')
            arr.append(x.split(','))
        return arr

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

    def logTemperature(self) -> int:
        num_entries = config.NUM_LOG_ROWS | 5

        header = ['timestamp', 'temperature']
        timestamp = self.getTimestamp()

        data = [timestamp, Temperature().read()]
        # data = [timestamp, 10]
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
            # csv.writeRow(b, bottle_list)
            csv.writeRow(b, header)
            csv.writeRow(b, data)

            for i in range(1, len(bottle_list)):
                if i > num_entries - 2:
                    break
                csv.writeRow(b, bottle_list[i])
        return timestamp

    def getTimestampFromLog(self) -> int | None:
        csv = Csv()
        bottle_list = []
        try:
            with open('log/temp.csv', 'r+') as b:
                bottles = csv.read(b)
                bottle_list.extend(bottles)
        except:
            # print('No data')
            return None
        try:
            # print(bottle_list[1][0])
            return int(bottle_list[1][0])
        except:
            # print('No data')
            return None

    def getTimestamp(self) -> int:
        time_stamp = time.mktime(time.gmtime())

        # time_stamp = current_time.timestamp()
        # print("timestamp:-", time_stamp)

        return time_stamp

    # broke
    def getTimeFromTimestamp(self, time_stamp) -> int:
        # date_time = datetime.fromtimestamp(time_stamp)
        # print("The date and time is:", date_time)
        return 1

    # def addSecs(self, org_time, secs) -> datetime:
    #     return datetime.timestamp(datetime.fromtimestamp(org_time) + timedelta(seconds=secs))

    def logComp(self, log, secToAdd) -> int | bool:
        # print(self.getTimestamp())
        # print((log))
        # print((log) + (secToAdd))
        time = self.getTimestamp()
        if log is None or time >= (log) + (secToAdd):
            # self.time_stamp = time
            return True
        else:
            return False
        # return (self.getTimestamp() >= self.time_stamp + (1000 * 60))


class Lamp:

    def toggle(self):
        print('toggle Led')
        led = Pin("LED", Pin.OUT)
        led.toggle()


class MatchTopic:
    def test(self, topic, target: str):
        try:
            return re.match(target, topic).group(0).split('/')
        except:
            return False
