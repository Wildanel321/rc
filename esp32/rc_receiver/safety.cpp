#include "safety.h"

static unsigned long lastPacketTime = 0;
static bool failsafeTriggered = false;

void initSafety() {
    lastPacketTime = millis();
    failsafeTriggered = false;
}

void resetWatchdog() {
    lastPacketTime = millis();
    if (failsafeTriggered) {
        Serial.println("[SAFETY] Valid packet received. Failsafe cleared.");
        failsafeTriggered = false;
    }
}

void updateSafety() {
    if (!failsafeTriggered && (millis() - lastPacketTime > FAILSAFE_TIMEOUT_MS)) {
        stopMotors();
        failsafeTriggered = true;
        Serial.println("[SAFETY] UDP Timeout (>300ms) - EMERGENCY STOP");
    }
}

bool isFailsafeActive() {
    return failsafeTriggered;
}
