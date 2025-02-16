import streamlit as st
import pandas as pd
import requests
import time

# Flask Server URL
SERVER_URL = "http://192.168.1.9:5001/latest"  # Replace with your actual PC IP

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