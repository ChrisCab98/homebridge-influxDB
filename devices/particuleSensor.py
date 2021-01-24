import json
import time
from datetime import datetime

from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector


class ParticuleSensor_Daemon(IMqttConnector):
    def __init__(self, topic, location):
        super().__init__()
        self.__location = location
        self.__topic = topic
        self.__mqtt = MqttClient(
            self,
            "homebridge.local",
            [
                self.__topic,
            ],
            "ParticuleSensor_Daemon" + self.__location,
        )
        self.__PM10 = 0.0
        self.__PM2_5 = 0.0
        self.__PM1 = 0.0
        self.__rawDatas = ""

        self.__now = datetime.utcnow().isoformat()
        self.__packet = ""
        self.__formattedData = []

    def rawDatas2PM10(self, H_D3, L_D3):
        PM10 = (H_D3 * 256) + L_D3
        print("PM10 : " + str(PM10) + " ug/m3")
        self.__PM10 = PM10

    def rawDatas2PM2_5(self, H_D2, L_D2):
        PM2_5 = (H_D2 * 256) + L_D2
        print("PM2.5 : " + str(PM2_5) + " ug/m3")
        self.__PM2_5 = PM2_5

    def rawDatas2PM1(self, H_D1, L_D1):
        PM1 = (H_D1 * 256) + L_D1
        print("PM1 : " + str(PM1) + " ug/m3")
        self.__PM1 = PM1

    def checkCS(self, datas):
        CS = sum()
        if datas["datas"]["CS"] == CS:
            return True
        else:
            return False

    def Receive(self, server, topic: str, payload: bytes):
        self.__client = InfluxDBClient("homebridge.local", port=8086)
        self.__client.switch_database("HomeKit")
        self.__now = datetime.utcnow().isoformat()

        print("[MQTT] " + topic)

        self.__packet = payload.decode("utf-8")
        self.__packet = json.loads(self.__packet)

        self.__bytearrayDatas = bytearray.fromhex(self.__packet["SerialReceived"])

        self.__formattedData = [
            {
                "headers": {
                    "Head1": self.__bytearrayDatas[0],
                    "Head2": self.__bytearrayDatas[1],
                },
                "datas": {
                    "H_Lenght": self.__bytearrayDatas[2],
                    "L_Lenght": self.__bytearrayDatas[3],
                    "H_D1": self.__bytearrayDatas[4],
                    "L_D1": self.__bytearrayDatas[5],
                    "H_D2": self.__bytearrayDatas[6],
                    "L_D2": self.__bytearrayDatas[7],
                    "H_D3": self.__bytearrayDatas[8],
                    "L_D3": self.__bytearrayDatas[9],
                    "H_D4": self.__bytearrayDatas[10],
                    "L_D4": self.__bytearrayDatas[11],
                    "H_D5": self.__bytearrayDatas[12],
                    "L_D5": self.__bytearrayDatas[13],
                    "H_D6": self.__bytearrayDatas[14],
                    "L_D6": self.__bytearrayDatas[15],
                    "H_D7": self.__bytearrayDatas[16],
                    "L_D7": self.__bytearrayDatas[17],
                    "H_D8": self.__bytearrayDatas[18],
                    "L_D8": self.__bytearrayDatas[19],
                    "H_D9": self.__bytearrayDatas[20],
                    "L_D9": self.__bytearrayDatas[21],
                    "H_D10": self.__bytearrayDatas[22],
                    "L_D10": self.__bytearrayDatas[23],
                    "H_D11": self.__bytearrayDatas[24],
                    "L_D11": self.__bytearrayDatas[25],
                    "H_D12": self.__bytearrayDatas[26],
                    "L_D12": self.__bytearrayDatas[27],
                    "H_D13": self.__bytearrayDatas[28],
                    "L_D13": self.__bytearrayDatas[29],
                    "H_CS": self.__bytearrayDatas[30],
                    "L_CS": self.__bytearrayDatas[31],
                },
            }
        ]

        self.rawDatas2PM10(
            self.__formattedData[0]["datas"]["H_D3"],
            self.__formattedData[0]["datas"]["L_D3"],
        )
        self.rawDatas2PM2_5(
            self.__formattedData[0]["datas"]["H_D2"],
            self.__formattedData[0]["datas"]["L_D2"],
        )
        self.rawDatas2PM1(
            self.__formattedData[0]["datas"]["H_D1"],
            self.__formattedData[0]["datas"]["L_D1"],
        )

        self.__jsonBody = [
            {
                "measurement": "Environment",
                "tags": {
                    "Location": self.__location,
                },
                "time": self.__now,
                "fields": {
                    "PM10": self.__PM10,
                    "PM2.5": self.__PM2_5,
                    "PM1": self.__PM1,
                },
            },
        ]

        self.__client.write_points(self.__jsonBody)
        self.__client.close()

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[{}] closed".format("ParticuleSensor_Daemon" + self.__location))
