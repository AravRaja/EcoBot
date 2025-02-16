import machine
import utime
import dht
import ujson  # For JSON formatting

# Set up the capacitive moisture sensors (3 sensors on ADC pins)
moisture_sensors = [
    machine.ADC(26),  # Quadrant 1
    machine.ADC(27),  # Quadrant 2
    machine.ADC(28)   # Quadrant 3
]

# Set up the DHT11 sensor on GP16
dht_sensor = dht.DHT11(machine.Pin(21))

# Function to read moisture sensors
def read_moisture(sensor):
    value = sensor.read_u16()
    percentage = 100 - ((value / 65535) * 100)  # Convert to % moisture
    return round(percentage, 2)

while True:
    try:
        # Read moisture from all 3 sensors
        moisture_levels = [read_moisture(sensor) for sensor in moisture_sensors]
        
        # Read temperature and humidity
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Create JSON object
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "moisture": moisture_levels
        }

        # Send JSON data
        print(ujson.dumps(data))  # Use print instead of sys.stdout.write()

        # Wait 2 seconds before next reading
        utime.sleep(2)

    except Exception as e:
        print("Error reading sensors:", str(e))  # Print directly
        utime.sleep(2)