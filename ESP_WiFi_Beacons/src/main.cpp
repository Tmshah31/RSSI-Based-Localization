#include <Arduino.h>
#include <WiFi.h>


const char * ssid = "ESP_Beacon_two"; //change according to the ESP
const char * password = "HelloTest2";



void setup() {
  Serial.begin(115200);

  // Start the ESP32 in Access Point mode
  WiFi.mode(WIFI_AP);
  bool result = WiFi.softAP(ssid, password,1); // start the AP on channel 1 no channel hoppin

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
  // ESP32 automatically sends beacons periodically
  delay(500);
}