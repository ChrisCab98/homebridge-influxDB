import json
import time
from datetime import datetime

from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector


class Humidity_Daemon(IMqttConnector):
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
            "Humidity_Daemon_" + self.__location,
        )
        self.__humidity = 0.0

        self.__now = datetime.utcnow().isoformat()
        self.__packet = ""

    def Receive(self, server, topic: str, payload: bytes):
        self.__client = InfluxDBClient("homebridge.local", port=8086)
        self.__client.switch_database("HomeKit")
        self.__now = datetime.utcnow().isoformat()

        print("[MQTT] " + topic)

        self.__packet = payload.decode("utf-8")
        print(self.__packet)

        self.__humidity = float(self.__packet)

        self.__jsonBody = [
            {
                "measurement": "Environment",
                "tags": {
                    "Location": self.__location,
                },
                "time": self.__now,
                "fields": {
                    "Humidity": self.__humidity,
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
        print("")
        # print("[Thermometer] with uniqueID {} closed".format(self.__uniqueID))
