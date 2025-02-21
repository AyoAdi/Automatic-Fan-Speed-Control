#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define DHTPIN 0
#define DHTTYPE DHT11

const int pirPin = 4;
const int relayPin = 5;
const int motorIn1 = 12;
const int motorIn2 = 13;
const int motorEnA = 15;

#define RELAY_ON LOW
#define RELAY_OFF HIGH

int pirState = LOW;
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Bharani Kumar";
const char* password = "Bharani2004";
const char* serverName = "http://192.168.96.45:5001/predict";
int motorSpeeds[] = {200, 190, 205, 255, 240, 255};
void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
  pinMode(relayPin, OUTPUT);
  pinMode(motorIn1, OUTPUT);
  pinMode(motorIn2, OUTPUT);
  pinMode(motorEnA, OUTPUT);
  dht.begin();
  digitalWrite(relayPin, RELAY_OFF);
  digitalWrite(motorIn1, LOW);
  digitalWrite(motorIn2, LOW);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}
void loop() {
  pirState = digitalRead(pirPin);
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  if (pirState == LOW) {
    digitalWrite(relayPin, RELAY_ON);
    digitalWrite(motorIn1, LOW);
    digitalWrite(motorIn2, LOW);
    analogWrite(motorEnA, 0);
  } else {
    digitalWrite(relayPin, RELAY_OFF);
    if (!isnan(temperature) && !isnan(humidity)) {
      int fanSpeed = sendToFlask(temperature, humidity);
      if (fanSpeed >= 0) {
        int motorSpeed = mapFanSpeedToPWM(fanSpeed);
        digitalWrite(motorIn1, HIGH);
        digitalWrite(motorIn2, LOW);
        analogWrite(motorEnA, motorSpeed);
        Serial.print("Mapped Motor PWM Speed: ");
        Serial.println(motorSpeed);
      } else {
        Serial.println("Failed to get fan speed from server");
      }
    }
  }
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  delay(2000);
}
int sendToFlask(float temperature, float humidity) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    String jsonPayload = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";
    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonPayload);
    int fanSpeed = -1;

    if (httpResponseCode > 0) {
      String response = http.getString();
      int fanSpeedIndex = response.indexOf("\"fanSpeed\": ");
      if (fanSpeedIndex != -1) {
        fanSpeed = response.substring(fanSpeedIndex + 12).toInt();
        Serial.println("Received Fan Speed from server: " + String(fanSpeed));
      } else {
        Serial.println("Fan speed not found in response");
      }
    } else {
      Serial.println("Error in sending POST request");
    }

    http.end();
    return fanSpeed;
  } else {
    Serial.println("WiFi not connected");
    return -1;
  }
}
int mapFanSpeedToPWM(int fanSpeed) {
  if (fanSpeed >= 1 && fanSpeed <= 6) {
    return motorSpeeds[fanSpeed - 1];
  } else {
    return motorSpeeds[0];
  }
}
