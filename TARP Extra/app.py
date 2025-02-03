from flask import Flask, request, jsonify
import pickle
import numpy as np

# Load your model
with open('dtf_updated.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return "ESP8266 Fan Speed Prediction Server"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temperature = float(data['temperature'])
    humidity = float(data['humidity'])

    input_data = np.array([[temperature, humidity]])
    fan_speed = int(model.predict(input_data)[0])  # Convert to int for JSON serialization
    return jsonify({'fanSpeed': fan_speed})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)




    