import network
import urequests
import machine
import utime
import dht
import ujson

# WiFi credentials (replace with your WiFi SSID and password)
SSID = "SHELL_0FC4"
PASSWORD = "5af5fc6cea324"

# Flask Server IP (Your PC's local IP)
SERVER_IP = "192.168.1.9"  # Change this to your actual PC IP
SERVER_PORT = 5001
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}/data"

# Set up WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
while not wlan.isconnected():
    utime.sleep(1)

print("✅ Connected to WiFi:", wlan.ifconfig())

# Set up the moisture sensors
moisture_sensors = [
    machine.ADC(26),
    machine.ADC(27),
    machine.ADC(28)
]

# Set up the DHT11 sensor
dht_sensor = dht.DHT11(machine.Pin(21))

# Function to read moisture sensors
def read_moisture(sensor):
    value = sensor.read_u16()
    percentage = 100 - ((value / 65535) * 100)
    return round(percentage, 2)

while True:
    try:
        # Read moisture sensors
        moisture_levels = [read_moisture(sensor) for sensor in moisture_sensors]

        # Read temperature and humidity
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Compute Dew Point
        dew_point = temperature - ((100 - humidity) / 5)

        # Compute Heat Index
        heat_index = temperature + (0.33 * humidity) - 0.7

        # Create JSON object
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "moisture": moisture_levels,
            "dew_point": round(dew_point, 2),
            "heat_index": round(heat_index, 2)
        }

        # Send data to Flask server
        response = urequests.post(SERVER_URL, json=data)
        print("✅ Sent Data:", ujson.dumps(data))
        response.close()

        utime.sleep(2)  # Adjust timing to prevent overload

    except Exception as e:
        print("❌ Error:", str(e))
        utime.sleep(2)