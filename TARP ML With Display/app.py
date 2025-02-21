from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS to allow cross-origin requests
import pickle
import numpy as np

# Load your model
with open('dtf_updated.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global dictionary to store the latest data
latest_data = {"temperature": None, "humidity": None, "fanSpeed": None}

@app.route('/')
def index():
    return render_template("index.html")  # Serve the HTML page

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temperature = float(data['temperature'])
    humidity = float(data['humidity'])

    input_data = np.array([[temperature, humidity]])
    fan_speed = int(model.predict(input_data)[0])  # Convert to int for JSON serialization

    # Store the latest data for retrieval
    latest_data.update({'temperature': temperature, 'humidity': humidity, 'fanSpeed': fan_speed})

    return jsonify(latest_data)

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
