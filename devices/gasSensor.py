import json
import time
from datetime import datetime

from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector


class GasSensor_Daemon(IMqttConnector):
    def __init__(self, topic, location):
        super().__init__()
        self.__location = location
        self.__topic = topic
        self.__TVOC = 0
        self.__eCO2 = 0
        self.__mqtt = MqttClient(
            self,
            "homebridge.local",
            [
                self.__topic,
            ],
            "GasSensor_Daemon-" + self.__location,
        )

        self.__now = datetime.utcnow().isoformat()
        self.__packet = ""

    def Receive(self, server, topic: str, payload: bytes):
        self.__client = InfluxDBClient("homebridge.local", port=8086)
        self.__client.switch_database("HomeKit")
        self.__now = datetime.utcnow().isoformat()

        print("[MQTT] " + topic)

        self.__packet = payload.decode("utf-8")
        print(self.__packet)
        data = json.loads(self.__packet)
        print(data)

        self.__TVOC = data["CCS811"]["TVOC"]
        self.__eCO2 = data["CCS811"]["eCO2"]

        self.__jsonBody = [
            {
                "measurement": "Environment",
                "tags": {
                    "Location": self.__location,
                },
                "time": self.__now,
                "fields": {"eCO2": self.__eCO2, "TVOC": self.__TVOC},
            },
        ]
        print(self.__jsonBody)

        self.__client.write_points(self.__jsonBody)
        self.__client.close()

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[{}] closed".format("GasSensor_Daemon-" + self.__location))