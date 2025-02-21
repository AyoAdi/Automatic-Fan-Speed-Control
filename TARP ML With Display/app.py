from flask import Flask, request, jsonify, render_template
from flask_cors import CORS 
import pickle
import numpy as np

with open('dtf_updated.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__)
CORS(app)  

latest_data = {"temperature": None, "humidity": None, "fanSpeed": None}
@app.route('/')
def index():
    return render_template("index.html") 

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temperature = float(data['temperature'])
    humidity = float(data['humidity'])

    input_data = np.array([[temperature, humidity]])
    fan_speed = int(model.predict(input_data)[0]) 

    latest_data.update({'temperature': temperature, 'humidity': humidity, 'fanSpeed': fan_speed})

    return jsonify(latest_data)

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
