from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests

# Load your ML model
with open('dtf_updated.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from ESP8266

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/set_fan_speed', methods=['POST'])
def set_fan_speed():
    data = request.get_json()
    mode = data.get('mode')
    esp8266_url = 'http://192.168.71.92/set_speed'  # Replace with the actual ESP8266 IP address

    try:
        if mode == 'auto':
            # Fetch dynamic temperature and humidity values
            temperature = data.get('temperature')
            humidity = data.get('humidity')

            if temperature is None or humidity is None:
                return jsonify({'error': 'Temperature and humidity required in auto mode'}), 400

            # Use the ML model to predict fan speed
            input_data = np.array([[float(temperature), float(humidity)]])
            fan_speed = int(model.predict(input_data)[0])
        elif mode == 'manual':
            fan_speed = int(data.get('fanSpeed'))
        else:
            return jsonify({'error': 'Invalid mode selected'}), 400

        # Send the fan speed to the ESP8266
        response = requests.post(esp8266_url, json={'fanSpeed': fan_speed})
        response.raise_for_status()

        return jsonify({'fanSpeed': fan_speed, 'espResponse': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
