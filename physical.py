import time
import serial.tools.list_ports
print("RS485")

try:
    ser = serial.Serial(port="COM4", baudrate=9600)
except:
    print("Can not open the port")

relay1_ON  = [0, 6, 0, 0, 0, 255, 200, 91]
relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

relay2_ON  = [15, 6, 0, 0, 0, 255, 200, 164]
relay2_OFF = [15, 6, 0, 0, 0, 0, 136, 228]

device1ON = False
device2ON = False

def setDevice2(state):
    if state == True:
        ser.write(relay2_ON)
        device2ON = True
    else:
        ser.write(relay2_OFF)

def setDevice1(state):
    if state == True:
        ser.write(relay1_ON)
        device1ON = True
    else:
        ser.write(relay1_OFF)

# while True:
#     setDevice1(True)
#     time.sleep(2)
#     setDevice1(False)
#     time.sleep(2)
#     setDevice2(True)
#     time.sleep(2)
#     setDevice2(False)
#     time.sleep(2)


import sys

import Adafruit_IO
from Adafruit_IO import MQTTClient
import time
import random
print('Run...')
# from Lab04 import facemark_detector

# AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_FEED_ID_1 = "nutnhan1"
AIO_FEED_ID_2 = "nutnhan2"
AIO_USERNAME = "ducminhquan"
AIO_KEY = "aio_wtbq49sdgZxYTn3pV4p3myL3OfUO"

def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

soil_temperature = [1,3,0,6,0,1,100,11]
def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)


soil_moisture = [1,3,0,7,0,1,53,203]
def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)

# Import standard python modules.
import sys

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'ducminhquan'

# Set to the ID of the feed to subscribe to for updates.


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(AIO_FEED_ID_1))
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(AIO_FEED_ID_2))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(AIO_FEED_ID_1)
    client.subscribe(AIO_FEED_ID_2)

def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(AIO_FEED_ID_1, granted_qos[0]))
    print('Subscribed to {0} with QoS {1}'.format(AIO_FEED_ID_2, granted_qos[0]))

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if feed_id == AIO_FEED_ID_1:
        setDevice1("1" == payload)
    else:
        setDevice2("1" == payload)

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
# client.on_message    = message
# client.on_subscribe  = subscribe

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
# client.loop_blocking()
aio = Adafruit_IO.Client(AIO_USERNAME, AIO_KEY)
counter = 10
while True:
    counter = counter - 1
    if counter <= 0:
        counter = 10
        # temp = random.randint(10, 20)
        # client.publish('cambien1', temp)
        # print('cambien1: ' + str(temp))
        # humi = random.randint(50, 70)
        # client.publish('cambien2', humi)
        # print('cambien2: ' + str(humi))
        # light = random.randint(100, 500)
        # client.publish('cambien3', light)
        # print('cambien3: ' + str(light))
        # if device1ON:
        value = readTemperature()
        print('Temperature value: ' + str(value))
        client.publish('cambien1', value)
        # if device2ON:
        value = readMoisture()
        print('Moisture value: ' + str(value))
        client.publish('cambien2', value)
    time.sleep(1)
    pass