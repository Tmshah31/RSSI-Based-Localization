#include <Arduino.h>
#include <WiFi.h>


const char * ssid = "ESP_Beacon_one";
const char * password = "HelloTest1";



void setup() {
  Serial.begin(115200);

  // Start the ESP32 in Access Point mode
  WiFi.mode(WIFI_AP);
  bool result = WiFi.softAP(ssid, password);

  if (result) {
    Serial.println("Access Point started successfully!");
    Serial.print("SSID: ");
    Serial.println(ssid);
    Serial.print("IP Address: ");
    Serial.println(WiFi.softAPIP());   // default is 192.168.4.1
  } else {
    Serial.println("Failed to start Access Point.");
  }
}

void loop() {
  // Nothing required — ESP32 automatically sends beacons periodically
  delay(1000);
}