#include <PubSubClient.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <IRremoteESP8266.h>
#include <MQTT.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "WifiAuth.h"

IRsend irsend(D1);

const char* host = "bed_room/#"; // the name of your fixture, and the base channel to listen to
IPAddress MQTTserver(10, 0, 1, 17);

WiFiClient wclient;
PubSubClient client(wclient, MQTTserver);

void setup_wifi()
{
  delay(10);
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.print(WiFi.localIP());
}

void setup_ir()
{
  Serial.println("Booting IR...");
  irsend.begin();
  Serial.println("IR online");
}

void setup() 
{
  Serial.begin(115200);
  Serial.println("Booting");

  setup_wifi();
  setup_ir();
  client.set_callback(callback);
}

void loop() 
{
  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      if (client.connect("ESP8266: Fountain - 2")) {
        client.subscribe(host);
        Serial.print("Connected to ");
        Serial.println(host);
      }
    }

    if (client.connected())
      client.loop();
  } else {
    Serial.println("Wifi not connected");
  }
}

unsigned int *integerArray(char *str, unsigned int *out_len) {
  char sep[] = ",";
  unsigned int count = 0;
  unsigned int *arr = NULL;
  char *pt;
  pt = strtok(str, sep);  
  
  do {
    count++;
    arr = (unsigned int*)realloc(arr, count * sizeof(*arr));
    arr[count - 1] = atoi(pt);
    pt = strtok(NULL, sep); 
  } while (pt != NULL);
  
  *out_len = count;
  return arr;
}

void sendIR(unsigned int *sequence, int len) 
{  
  const unsigned int hz = 38;
  Serial.print("Sending ");
  Serial.print(len);
  Serial.println(" IR commands");
  irsend.sendRaw(sequence, len, hz);
  Serial.println("IR sent");
}

void callback(const MQTT::Publish& pub) {
  // handle message arrived
  Serial.print(pub.topic());
  Serial.print(" => ");
  Serial.println(pub.payload_string());

  unsigned int *sequence;
  unsigned int len;
  sequence = integerArray((char*)pub.payload_string().c_str(), &len);
  Serial.print("Parsed sequence with length: ");
  Serial.println(len);
  
  sendIR(sequence, len);
}

