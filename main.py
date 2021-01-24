from devices.gasSensor import GasSensor_Daemon
from devices.humidity import Humidity_Daemon
from devices.particuleSensor import ParticuleSensor_Daemon
from devices.thermometer import Thermometer_Daemon
from homebridge.queryParticuleSensor import QueryParticuleSensor

G_Daemon = GasSensor_Daemon("tele/tasmota_C34BE1/SENSOR", "Bedroom")
# P_Daemon = ParticuleSensor_Daemon("SM-UART-04L/RESULT","Bedroom")

# query = QueryParticuleSensor("stat/SM-UART-04L/RESULT/", "bedroom")
# query.queryPM10()
# query.queryPM2_5()
# query.sendAirQualityValues()

# query.halt()


# print("bonjour")

# H_Daemon_Bedroom = Humidity_Daemon("getCurrentRelativeHumidity/TRIO2SYS","Bedroom")
# H_Daemon_LivingRoom = Humidity_Daemon("getCurrentRelativeHumidity2/TRIO2SYS","Living Room")

# T_Daemon_Bedroom = Thermometer_Daemon("getCurrentTemperature/TRIO2SYS","Bedroom")
# T_Daemon_LivingRoom = Thermometer_Daemon("getCurrentTemperature2/TRIO2SYS","Living Room")
