
  /////////////////////////////////////////////////////////////////
/*
  Broadcasting Your Voice with ESP32-S3 & INMP441
  For More Information: https://youtu.be/qq2FRv0lCPw
  Created by Eric N. (ThatProject)
*/
/////////////////////////////////////////////////////////////////

/*
- Device
ESP32-S3 DevKit-C
https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html

- Required Library
Arduino ESP32: 2.0.9

Arduino Websockets: 0.5.3
https://github.com/gilmaimon/ArduinoWebsockets
*/


#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <Arduino.h>

#define MQ4_DO_PIN 27  // Digital pin for MQ4 sensor
#define MQ4_AO_PIN 32  // Analog pin for MQ4 sensor (adjust as needed)


const char* ssid = "Areete";
const char* password = "areete@321#";

const char* websocket_server_host = "192.168.0.224";
const uint16_t websocket_server_port = 8888;  // <WEBSOCKET_SERVER_PORT>

using namespace websockets;
WebsocketsClient client;
bool isWebSocketConnected;

void onEventsCallback(WebsocketsEvent event, String data) {
  if (event == WebsocketsEvent::ConnectionOpened) {
    Serial.println("Connnection Opened");
    isWebSocketConnected = true;
  } else if (event == WebsocketsEvent::ConnectionClosed) {
    Serial.println("Connnection Closed");
    isWebSocketConnected = false;
  } else if (event == WebsocketsEvent::GotPing) {
    Serial.println("Got a Ping!");
  } else if (event == WebsocketsEvent::GotPong) {
    Serial.println("Got a Pong!");
  }
}



void setup() {
  Serial.begin(115200);
  pinMode(MQ4_DO_PIN, INPUT);  // Set the digital pin as input

  connectWiFi();
  connectWSServer();
  xTaskCreatePinnedToCore(micTask, "micTask", 10000, NULL, 1, NULL, 1);
}

void loop() {
}

void connectWiFi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void connectWSServer() {
  client.onEvent(onEventsCallback);
  while (!client.connect(websocket_server_host, websocket_server_port, "/")) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Websocket Connected!");
}


void micTask(void* parameter) {

  

  size_t bytesIn = 0;
  while (1) {int analogValue = analogRead(MQ4_AO_PIN);  // Read the analog value from the sensor
  float voltage = analogValue * (3.3 / 4095.0);  // Convert analog value to voltage (3.3V reference)
  
  // Convert voltage to methane concentration in ppm (parts per million)
  // This conversion formula needs to be adjusted based on sensor calibration
  float methanePPM = voltage * 10;
  String strout = String(methanePPM);
  client.send(strout);
    // Adjust delay based on your application needs
  }
}
  
