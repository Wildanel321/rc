#include "network.h"

static WiFiUDP udp;
static char packetBuffer[256];
static bool wasConnected = false;

void initNetwork() {
    Serial.println("[WiFi] Connecting to AP...");
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    unsigned long startAttempt = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < 10000) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();

    if (WiFi.status() == WL_CONNECTED) {
        wasConnected = true;
        Serial.println("[WiFi] Connected");
        Serial.print("[WiFi] IP: ");
        Serial.println(WiFi.localIP());

        udp.begin(UDP_PORT);
        Serial.print("[UDP] Listening on port ");
        Serial.println(UDP_PORT);
        Serial.println("[RC] READY");
    } else {
        Serial.println("[WiFi] Connection initial attempt timeout. Will continue retrying in loop.");
    }
}

static void parseControlPayload(const char* payload) {
    // Parse JSON object
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, payload);

    if (error) {
        // Ignored invalid JSON format
        return;
    }

    const char* type = doc["type"];
    if (!type || strcmp(type, "control") != 0) {
        return;
    }

    int left_motor = 0;
    int right_motor = 0;

    // Support both direct motor (left, right) or throttle/steering fields
    if (doc.containsKey("throttle") && doc.containsKey("steering")) {
        int throttle = doc["throttle"];
        int steering = doc["steering"];

        // Input Validation
        if (throttle < -100 || throttle > 100 || steering < -100 || steering > 100) {
            Serial.println("[WARN] Invalid range in throttle/steering packet. Ignored.");
            return;
        }

        // Differential calculation
        left_motor = constrain(throttle + steering, -100, 100);
        right_motor = constrain(throttle - steering, -100, 100);
    } else if (doc.containsKey("left") && doc.containsKey("right")) {
        left_motor = doc["left"];
        right_motor = doc["right"];

        // Input Validation
        if (left_motor < -100 || left_motor > 100 || right_motor < -100 || right_motor > 100) {
            Serial.println("[WARN] Invalid range in left/right motor packet. Ignored.");
            return;
        }
    } else {
        return;
    }

    // Packet validated successfully -> Reset watchdog and update motors
    resetWatchdog();
    setMotors(left_motor, right_motor);
}

void updateNetwork() {
    // Check Wi-Fi Connection state
    if (WiFi.status() != WL_CONNECTED) {
        if (wasConnected) {
            wasConnected = false;
            stopMotors();
            Serial.println("[WiFi] Connection lost");
            Serial.println("[SAFETY] Motors stopped");
            Serial.println("[WiFi] Reconnecting...");
        }
        WiFi.reconnect();
        delay(100);
        return;
    } else {
        if (!wasConnected) {
            wasConnected = true;
            Serial.println("[WiFi] Connected");
            Serial.print("[WiFi] IP: ");
            Serial.println(WiFi.localIP());
            Serial.println("[RC] Waiting for valid controller packet...");
        }
    }

    // Listen for UDP Packets
    int packetSize = udp.parsePacket();
    if (packetSize > 0) {
        int len = udp.read(packetBuffer, sizeof(packetBuffer) - 1);
        if (len > 0) {
            packetBuffer[len] = 0;
            parseControlPayload(packetBuffer);
        }
    }
}

void checkSerialCommands() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        if (input.length() == 0) return;

        Serial.print("[TEST COMMAND] Received: ");
        Serial.println(input);

        int spaceIndex = input.indexOf(' ');
        String cmd = (spaceIndex != -1) ? input.substring(0, spaceIndex) : input;
        int val = (spaceIndex != -1) ? input.substring(spaceIndex + 1).toInt() : 0;

        cmd.toLowerCase();
        if (cmd == "forward") {
            resetWatchdog();
            setMotors(val, val);
        } else if (cmd == "reverse") {
            resetWatchdog();
            setMotors(-val, -val);
        } else if (cmd == "left") {
            resetWatchdog();
            setMotors(-val, val);
        } else if (cmd == "right") {
            resetWatchdog();
            setMotors(val, -val);
        } else if (cmd == "stop") {
            stopMotors();
        } else {
            Serial.println("Unknown command. Valid commands: forward <speed>, reverse <speed>, left <speed>, right <speed>, stop");
        }
    }
}
