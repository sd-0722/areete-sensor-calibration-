#define MQ4_DO_PIN 27  // Digital pin for MQ4 sensor
#define MQ4_AO_PIN 32  // Analog pin for MQ4 sensor (adjust as needed for your ESP32 board)

void setup() {
  Serial.begin(115200);  // Initialize serial communication at 115200 baud rate
  pinMode(MQ4_DO_PIN, INPUT);  // Set the digital pin as input
}

void loop() {
  // Read the digital value from the sensor
  int sensorStatus = digitalRead(MQ4_DO_PIN);

  // Read the analog value from the sensor
  int analogValue = analogRead(MQ4_AO_PIN);  // Read the analog value from the sensor
  float voltage = analogValue * (3.3 / 4095.0);  // Convert analog value to voltage (3.3V reference)
  
  // Convert voltage to methane concentration in ppm (parts per million)
  // This conversion formula needs to be adjusted based on sensor calibration
  float methanePPM = voltage * 10;  // Example conversion (you need to calibrate this)

  // Print the digital status
  if (sensorStatus == HIGH) {
    Serial.println("Methane detected!");
  } else {
    Serial.println("Methane not detected.");
  }

  // Print the analog value, voltage, and methane concentration
  Serial.print("Analog Value: ");
  Serial.print(analogValue);
  Serial.print("\t Voltage: ");
  Serial.print(voltage);
  Serial.print(" V\t Methane PPM: ");
  Serial.println(methanePPM);
  
  delay(1000);  // Wait for 1 second before the next reading
}
