'''
import streamlit as st
import pandas as pd
import requests
import time

# Flask Server URL
SERVER_URL = "http://192.168.1.10:5001/latest"  # Replace with your actual PC IP

st.title("🌿 EcoBot Sensor Dashboard")
st.markdown("### Real-Time Sensor Readings from Raspberry Pi Pico WH")

# Initialize DataFrame
sensor_data = pd.DataFrame(columns=["Timestamp", "Temperature (°C)", "Humidity (%)", 
                                    "Moisture 1 (%)", "Moisture 2 (%)", "Moisture 3 (%)",
                                    "Dew Point (°C)", "Heat Index (°C)"])

# Create placeholders
temp_placeholder = st.metric(label="🌡️ Temperature (°C)", value="Waiting...")
humidity_placeholder = st.metric(label="💧 Humidity (%)", value="Waiting...")
moisture1_placeholder = st.metric(label="🪴 Moisture Sensor 1 (%)", value="Waiting...")
moisture2_placeholder = st.metric(label="🪴 Moisture Sensor 2 (%)", value="Waiting...")
moisture3_placeholder = st.metric(label="🪴 Moisture Sensor 3 (%)", value="Waiting...")
dew_point_placeholder = st.metric(label="☁️ Dew Point (°C)", value="Waiting...")
heat_index_placeholder = st.metric(label="🔥 Heat Index (°C)", value="Waiting...")
chart_placeholder = st.line_chart([])

while True:
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            data = response.json()

            timestamp = time.strftime("%H:%M:%S")

            temp_placeholder.metric("🌡️ Temperature (°C)", data["temperature"])
            humidity_placeholder.metric("💧 Humidity (%)", data["humidity"])
            moisture1_placeholder.metric("🪴 Moisture Sensor 1 (%)", data["moisture"][0])
            moisture2_placeholder.metric("🪴 Moisture Sensor 2 (%)", data["moisture"][1])
            moisture3_placeholder.metric("🪴 Moisture Sensor 3 (%)", data["moisture"][2])
            dew_point_placeholder.metric("☁️ Dew Point (°C)", data["dew_point"])
            heat_index_placeholder.metric("🔥 Heat Index (°C)", data["heat_index"])

            new_data = pd.DataFrame([[timestamp, data["temperature"], data["humidity"], 
                                      data["moisture"][0], data["moisture"][1], data["moisture"][2], 
                                      data["dew_point"], data["heat_index"]]],
                                    columns=sensor_data.columns)

            sensor_data = pd.concat([sensor_data, new_data], ignore_index=True)
            chart_placeholder.line_chart(sensor_data.set_index("Timestamp"))

        time.sleep(2)

    except Exception as e:
        st.warning(f"Error fetching data: {e}")
'''

import streamlit as st
import pandas as pd
import requests
import time

# Flask Server URL
SERVER_URL = "http://192.168.1.10:5001/latest"  # Replace with your actual PC IP

st.title("🌿 EcoBot Sensor Dashboard")
st.markdown("### Real-Time Sensor Readings from Raspberry Pi Pico WH")

# Explanation Section
st.markdown("""
### 🌍 Sensor Descriptions
- **🌡️ Temperature (°C):** Measures ambient temperature.
- **💧 Humidity (%):** Indicates the amount of moisture in the air.
- **🪴 Zone 1 Moisture (%):** Soil moisture level in zone 1.
- **🪴 Zone 2 Moisture (%):** Soil moisture level in zone 2.
- **🪴 Zone 3 Moisture (%):** Soil moisture level in zone 3.
- **☁️ Dew Point (°C):** Temperature at which dew forms.
""")

# Initialize DataFrame
sensor_data = pd.DataFrame(columns=["Timestamp", "Temperature (°C)", "Humidity (%)", 
                                    "Zone 1 Moisture (%)", "Zone 2 Moisture (%)", "Zone 3 Moisture (%)",
                                    "Dew Point (°C)"])

# Optimal values for sensor readings
OPTIMAL_VALUES = {
    "temperature": 20,
    "humidity": 52,
    "moisture": [34.33, 32.7, 34.07],
    "dew_point": 10.4
}

# Define state thresholds and colors
STATE_THRESHOLDS = {
    "normal": (10, "#2ecc71", "✅"),
    "inoptimal": (15, "#f1c40f", "⚠️"),
    "bad": (20, "#e67e22", "❗"),
    "critical": (30, "#e74c3c", "🚨")
}

# Function to determine state and color
def get_state(metric, value, index=None):
    try:
        optimal = OPTIMAL_VALUES[metric] if index is None else OPTIMAL_VALUES[metric][index]
        deviation = abs(value - optimal)
        
        for state, (threshold, color, emoji) in STATE_THRESHOLDS.items():
            if deviation <= threshold:
                return f"{emoji} {state.capitalize()}", color
        return "🚨 Critical", "#e74c3c"
    except KeyError:
        return "❓ Unknown", "#95a5a6"

# Create placeholders for sensor states (persists across updates)
state_placeholders = []
cols = st.columns(6)  # Reduced to 6 columns

button_style = "background-color:{}; padding: 15px; border-radius: 10px; text-align: center; color: white; font-size: 16px; width: 100%; display: flex; justify-content: center; align-items: center; min-height: 50px;"
label_style = "font-size: 12px; font-weight: bold; text-align: center;"

for i, (metric, key, index, label) in enumerate([
    ("temperature", "temperature", None, "🌡️ Temperature "),
    ("humidity", "humidity", None, "💧 Humidity Level"),
    ("moisture1", "moisture", 0, "🪴 Zone 1 Moisture"),
    ("moisture2", "moisture", 1, "🪴 Zone 2 Moisture"),
    ("moisture3", "moisture", 2, "🪴 Zone 3 Moisture"),
    ("dew_point", "dew_point", None, "☁️ Dew Form Point")]):  # Removed heat index

    with cols[i]:
        st.markdown(f"<div style='{label_style}'>{label}</div>", unsafe_allow_html=True)
        state_placeholder = st.empty()  # Create an empty placeholder
        state_placeholders.append(state_placeholder)

# Add spacing before charts
st.markdown("---")

# Placeholders for graphs
general_chart_placeholder = st.empty()
moisture_chart_placeholder = st.empty()

while True:
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            data = response.json()
            timestamp = time.strftime("%H:%M:%S")

            # Update sensor states dynamically
            for i, (metric, key, index, _) in enumerate([
                ("temperature", "temperature", None, "🌡️ Temperature "),
                ("humidity", "humidity", None, "💧 Humidity Level"),
                ("moisture1", "moisture", 0, "🪴 Zone 1 Moisture"),
                ("moisture2", "moisture", 1, "🪴 Zone 2 Moisture"),
                ("moisture3", "moisture", 2, "🪴 Zone 3 Moisture"),
                ("dew_point", "dew_point", None, "☁️ Dew Form Point")]):  # Removed heat index

                value = data.get(key, [None]*3)[index] if index is not None else data.get(key, None)
                if value is not None:
                    state, color = get_state(key, value, index)
                    state_placeholders[i].markdown(
                        f"<div style='{button_style.format(color)}'>{state}</div>",
                        unsafe_allow_html=True
                    )

            # Update sensor data
            new_data = pd.DataFrame([[timestamp, data.get("temperature", None), data.get("humidity", None), 
                                      data.get("moisture", [None, None, None])[0], 
                                      data.get("moisture", [None, None, None])[1], 
                                      data.get("moisture", [None, None, None])[2], 
                                      data.get("dew_point", None)]],  # Removed heat index
                                    columns=sensor_data.columns)
            
            sensor_data = pd.concat([sensor_data, new_data], ignore_index=True)

            # Ensure proper spacing before graphs
            st.markdown("---")

            # Update graphs dynamically
            general_chart_placeholder.line_chart(sensor_data.set_index("Timestamp")[["Temperature (°C)", "Humidity (%)", "Dew Point (°C)"]])  # Removed heat index
            moisture_chart_placeholder.line_chart(sensor_data.set_index("Timestamp")[["Zone 1 Moisture (%)", "Zone 2 Moisture (%)", "Zone 3 Moisture (%)"]])

        time.sleep(2)
    
    except Exception as e:
        st.warning(f"Error fetching data: {e}")


