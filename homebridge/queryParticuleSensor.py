import json
import time
from datetime import datetime

from influxdb import InfluxDBClient
from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector

# PM10
# excellent-value   (0 < PM10 < 50)
# good-value        (51 < PM10 < 100)
# fair-value        (101 < PM10 < 250)
# inferior-value    (251 < PM10 < 350)
# poor-value        (351 < PM10 < 430)

# PM2.5
# excellent-value   (0 < PM10 < 30)
# good-value        (31 < PM10 < 60)
# fair-value        (61 < PM10 < 90)
# inferior-value    (91 < PM10 < 120)
# poor-value        (121 < PM10 < 250)


class QueryParticuleSensor(IMqttConnector):
    def __init__(self, topic, location):
        super().__init__()
        self.__location = location
        self.__topic = topic
        self.__mqtt = MqttClient(
            self,
            "homebridge.local",
            [],
            "QueryParticuleSensor_Daemon" + self.__location,
        )
        self.__queryPM10 = 'SELECT mean("PM10") FROM "Environment" WHERE ("Location" = \'Bedroom\') AND time >= now() - 1h GROUP BY time(15m) LIMIT 1'
        self.__queryPM2_5 = 'SELECT mean("PM2.5") FROM "Environment" WHERE ("Location" = \'Bedroom\') AND time >= now() - 1h GROUP BY time(15m) LIMIT 1'
        self.__bind_params = {"location": self.__location}
        self.__PM10 = 0
        self.__PM2_5 = 0
        self.__airQualityValues = [
            "excellent-value",
            "good-value",
            "fair-value",
            "inferior-value",
            "poor-value",
            "unknown-value",
        ]
        self.__topicPM10 = "getPM10Density"
        self.__topicPM2_5 = "getPM2_5Density"
        self.__topicAirQualityValues = "getAirQuality"

    def Receive(self, server, topic: str, payload: bytes):
        print("Receive")

    def Send(self, topic, msg):
        print(topic)
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[{}] closed".format("ParticuleSensor_Daemon" + self.__location))

    def queryPM10(self):
        self.__client = InfluxDBClient("homebridge.local", 8086)
        self.__client.switch_database("HomeKit")
        result = self.__client.query(self.__queryPM10, bind_params=self.__bind_params)
        self.__PM10 = int(result.raw["series"][0]["values"][0][1])
        self.__client.close()

        print("PM10 : " + str(self.__PM10))

        self.Send(
            self.__topic + self.__topicPM10,
            self.__PM10,
        )
        time.sleep(1)

    def queryPM2_5(self):
        self.__client = InfluxDBClient("homebridge.local", 8086)
        self.__client.switch_database("HomeKit")
        result = self.__client.query(self.__queryPM2_5, bind_params=self.__bind_params)
        self.__PM2_5 = int(result.raw["series"][0]["values"][0][1])
        self.__client.close()

        print("PM2.5 : " + str(self.__PM2_5))

        self.Send(
            self.__topic + self.__topicPM2_5,
            self.__PM2_5,
        )
        time.sleep(1)

    def sendAirQualityValues(self):
        if (
            0 < self.__PM10
            and self.__PM10 < 50
            and 0 < self.__PM2_5
            and self.__PM2_5 < 30
        ):
            print(self.__airQualityValues[0])
            self.Send(
                self.__topic + self.__topicAirQualityValues,
                self.__airQualityValues[0],
            )
        else:
            if (
                51 < self.__PM10
                and self.__PM10 < 100
                and 31 < self.__PM2_5
                and self.__PM2_5 < 60
            ):
                print(self.__airQualityValues[1])
                self.Send(
                    self.__topic + self.__topicAirQualityValues,
                    self.__airQualityValues[1],
                )

            else:
                if (
                    101 < self.__PM10
                    and self.__PM10 < 250
                    and 61 < self.__PM2_5
                    and self.__PM2_5 < 90
                ):
                    print(self.__airQualityValues[2])
                    self.Send(
                        self.__topic + self.__topicAirQualityValues,
                        self.__airQualityValues[2],
                    )

                else:
                    if (
                        251 < self.__PM10
                        and self.__PM10 < 350
                        and 91 < self.__PM2_5
                        and self.__PM2_5 < 120
                    ):
                        print(self.__airQualityValues[3])
                        self.Send(
                            self.__topic + self.__topicAirQualityValues,
                            self.__airQualityValues[3],
                        )

                    else:
                        if (
                            351 < self.__PM10
                            and self.__PM10 < 430
                            and 121 < self.__PM2_5
                            and self.__PM2_5 < 250
                        ):
                            print(self.__airQualityValues[4])
                            self.Send(
                                self.__topic + self.__topicAirQualityValues,
                                self.__airQualityValues[4],
                            )
                        else:
                            print(self.__airQualityValues[5])
                            self.Send(
                                self.__topic + self.__topicAirQualityValues,
                                self.__airQualityValues[5],
                            )
        time.sleep(1)

    def halt(self):
        self.__mqtt.Halt()
