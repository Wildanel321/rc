#ifndef NETWORK_H
#define NETWORK_H

#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include "config.h"
#include "motor.h"
#include "safety.h"

void initNetwork();
void updateNetwork();
void checkSerialCommands();

#endif // NETWORK_H
