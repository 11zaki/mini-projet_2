import blynklib_mp as blynklib
import network
import utime as time
from machine import Pin
import dht

WIFI_SSID = 'HUAWEI P20 lite'
WIFI_PASS = 'ouni2021'
BLYNK_AUTH = 'X2C6yEvQ1NFYzW7vyUxiq94IJ9myQMyo'
GPIO_DHT11_PIN = 15

print("Connecting to WiFi network '{}'".format(WIFI_SSID))
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    time.sleep(1)
    print('WiFi connect retry ...')
print('WiFi IP:', wifi.ifconfig()[0])

print("Connecting to Blynk server...")
blynk = blynklib.Blynk(BLYNK_AUTH)

T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'

T_VPIN = 3
H_VPIN = 4

dht11 = dht.DHT11(Pin(15, Pin.IN, Pin.PULL_UP))


@blynk.handle_event('read V{}'.format(T_VPIN))
def read_handler(vpin):
    temperature = 0.0
    humidity = 0.0

    # read sensor data
    try:
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()
    except OSError as o_err:
        print("Unable to get DHT11 sensor data: '{}'".format(o_err))

    # change widget values and colors according read results
    if temperature != 0.0 and humidity != 0.0:
        blynk.set_property(T_VPIN, 'color', T_COLOR)
        blynk.set_property(H_VPIN, 'color', H_COLOR)
        blynk.virtual_write(T_VPIN, temperature)
        blynk.virtual_write(H_VPIN, humidity)


while True:
    blynk.run()
    humidity=dht11.humidity()
    print('Humidity: %3.1f %%' %humidity)
    temperature=dht11.temperature()
    print('temperature: %3.1f °C' %temperature) 
