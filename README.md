# HomeKit using Arduino and Raspberry Pi

This is a living document to track my progress, success, and failure at building a HomeKit-powered Infrared (IR) emitter to power appliances like my TV and air conditioner

## Components List

Right now this is just a list of the things I bought. It is **not** a bare-minimum setup.

- [400 point breadboard](https://www.amazon.com/gp/product/B004RXKWDQ/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) $3.99
- [NodeCMU v2](https://www.amazon.com/gp/product/B010O1G1ES/ref=oh_aui_search_detailpage?ie=UTF8&psc=1) $8.79 (aka ESP8266)
- [Raspberry Pi starter kit](https://www.amazon.com/gp/product/B01D92SSX6/ref=oh_aui_detailpage_o02_s01?ie=UTF8&psc=1) $49.99
- [Micro SD card 8gb](https://www.amazon.com/Kingston-microSDHC-Class-Memory-SDC4/dp/B00200K1TS/ref=sr_1_3?s=pc&ie=UTF8&qid=1484098805&sr=1-3&keywords=micro+sd+card+8gb) $4.99
- [Stick-on IR emitter](https://www.amazon.com/gp/product/B004WLATRC/ref=oh_aui_detailpage_o02_s01?ie=UTF8&psc=1) $9.19

## Software

- [HAP-NodeJS](https://github.com/KhaosT/HAP-NodeJS) installed on the Raspberry Pi to be a HomeKit server
- [IRremoteESP8266](https://github.com/markszabo/IRremoteESP8266) to send IR from the ESP8266
- [Download NodeJS](https://nodejs.org/en/download/) find "All download options" and download the `node-vX.X.X-linux-armv7l.tar.gz`

## Helpful Links

- [ESP8266 pins](https://github.com/esp8266/Arduino/blob/master/variants/nodemcu/pins_arduino.h#L37-L59)
- [ESP8266 pin diagram](https://cloud.githubusercontent.com/assets/2471931/7339810/935456c8-ec7b-11e4-9fa7-43d9c57b840a.png)
- [Setting up Arduino IDE for ESP8266](https://www.hackster.io/Aritro/getting-started-with-esp-nodemcu-using-arduinoide-aa7267)
- [Using MQTT with HAP-NodeJS accessory](https://gist.githubusercontent.com/jamesabruce/a6607fa9d93e41042fee/raw/12e4fd1d1c2624e7540ba5e17c3e79bc6bdec5fd/Officelight_accessory.js)
- [HomeKit + RaspberryPi tutorial](http://www.makeuseof.com/tag/make-diy-siri-controlled-wi-fi-light/)
