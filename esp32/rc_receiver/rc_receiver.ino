#include <Arduino.h>
#include "config.h"
#include "motor.h"
#include "safety.h"
#include "network.h"

void setup() {
    Serial.begin(SERIAL_BAUD);
    delay(500);

    Serial.println("\n==========================================");
    Serial.println("  Wi-Fi RC Receiver - ESP32 + L298N Firmware");
    Serial.println("==========================================");

    // Initialize Motor Control (Default STOP)
    initMotors();

    // Initialize Failsafe Watchdog
    initSafety();

    // Initialize Network Wi-Fi & UDP Listener
    initNetwork();
}

void loop() {
    // Process Network UDP Packets
    updateNetwork();

    // Check Failsafe Watchdog Timer (300 ms Timeout)
    updateSafety();

    // Check Serial Debugger / Test Commands
    checkSerialCommands();

    // Small yield for system stability
    delay(1);
}
