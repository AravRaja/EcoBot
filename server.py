from flask import Flask, request, jsonify

app = Flask(__name__)

# Store latest sensor data
sensor_data = {}

@app.route('/data', methods=['POST'])
def receive_data():
    global sensor_data
    sensor_data = request.json
    print("📩 Received Data:", sensor_data)
    return jsonify({"status": "success"}), 200

@app.route('/latest', methods=['GET'])
def get_latest_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)