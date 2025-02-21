# Fan Speed Control System

## Project Overview
This project is a fan speed control system that utilizes an ML model to predict fan speed based on temperature and humidity values. The system integrates an Arduino board, a web-based dashboard, and a local server running on Python with Flask. The ML model processes sensor data and adjusts the fan speed accordingly.

## Features
- **Automatic Fan Speed Control**: Uses a trained ML model (`dtf_updated.pkl`) to predict the fan speed based on temperature and humidity values.
- **Manual Control Mode**: Allows users to manually set the fan speed via the web interface.
- **Web Dashboard**: Displays real-time temperature, humidity, and fan speed values.
- **Arduino Integration**: Reads sensor data, sends it to the ML model, and receives the predicted fan speed to control the fan.

## File Structure
```
project_root/
│── app.py               # Flask backend
│── requirements.txt     # Required dependencies
│
├── templates/
│   └── chatbot.html     # Frontend UI (HTML + CSS + JS)
│
└── aws_lambda/          # AWS Lambda function (not included in repo)
```

## How It Works
1. The Arduino board is connected to a local network (hotspot).
2. The Arduino reads temperature and humidity values from its sensors.
3. The sensor data is sent to the Python Flask server (`app.py`), which loads the trained ML model (`dtf_updated.pkl`).
4. The model predicts the fan speed and sends it back to the Arduino.
5. The web dashboard (`chatbot.html`) fetches and displays the real-time temperature, humidity, and fan speed values.
6. Users can also manually set the fan speed through the dashboard.

## Setting Up the Project
### Prerequisites
- Python 3
- Flask (`pip install flask`)
- Scikit-learn (`pip install scikit-learn`)
- Arduino IDE
- ESP8266/ESP32 or compatible Wi-Fi module

### Getting the Arduino IP Address
Since the Arduino board is connected to a local network, it gets an IP address assigned automatically. You can find the IP address using the following code:

```cpp
#include <ESP8266WiFi.h>  // Use <WiFi.h> for ESP32

const char* ssid = "Your_SSID";
const char* password = "Your_PASSWORD";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.print("Connected! IP Address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
    // Empty loop
}
```

Once you obtain the IP address, enter it in `app.py` to allow the Flask server to communicate with the Arduino.

## Running the Project
1. **Upload `Arduino.ino` to the Arduino board.**
2. **Run the Flask server:**
   ```bash
   python app.py
   ```
3. **Open `chatbot.html` in a web browser** to view real-time data and control the fan.

## Future Improvements
- Implementing MQTT for more robust communication.
- Adding a mobile app for remote control.
- Expanding to more environmental parameters for better predictions.

## License
This project is open-source and can be modified as needed.

