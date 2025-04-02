import network
import urequests
from time import sleep
from machine import Pin, I2C, ADC
import ssd1306

# Wi-Fi Credentials
ssid = "..."
password = "..."

# ThingSpeak API Details
server = "http://api.thingspeak.com"
apikey = "..."
field_water = 1  # Water level to field 1

# Define Water Level Thresholds
LOW_THRESHOLD = 2500   # Adjust based on calibration
HIGH_THRESHOLD = 15000  # Adjust based on calibration

# GPIO Setup
water_sensor = ADC(Pin(26))  # Hoya Water Sensor on ADC0 (GP26)
buzzer = Pin(16, Pin.OUT)
green_led = Pin(14, Pin.OUT)
red_led = Pin(15, Pin.OUT)

# I2C Setup for OLED
i2c = I2C(0, scl=Pin(13), sda=Pin(12))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def ConnectWiFi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    print(f"Connected on {wlan.ifconfig()[0]}")

# Connect to Wi-Fi
ConnectWiFi()

# Function to update ThingSpeak
def send_to_thingspeak(value):
    url = f"{server}/update?api_key={apikey}&field{field_water}={value}"
    try:
        response = urequests.get(url, timeout=5)
        print(f"Sent to ThingSpeak: {value} | HTTP {response.status_code}")
        response.close()
    except Exception as e:
        print(f"Error sending data: {e}")

# Main Loop
last_level = -1  # Track last water level to avoid redundant updates
while True:
    water_level = water_sensor.read_u16()
    print(f"Water Level: {water_level}")

    # Determine status
    if water_level < LOW_THRESHOLD:
        status = "LOW!"
        red_led.on()
        green_led.off()
        buzzer.on()
    elif water_level > HIGH_THRESHOLD:
        status = "HIGH!"
        red_led.on()
        green_led.off()
        buzzer.on()
    else:
        status = "OK"
        red_led.off()
        green_led.on()
        buzzer.off()

    # Display on OLED
    oled.fill(0)
    oled.text("Water Level:", 10, 0)
    oled.text(f"{water_level}", 10, 20)
    oled.text(f"Status: {status}", 10, 40)
    oled.show()

    # Send to ThingSpeak if changed or every 30s
    if water_level != last_level or (time.ticks_ms() % 30000 == 0):
        send_to_thingspeak(water_level)
        last_level = water_level

    sleep(5)
