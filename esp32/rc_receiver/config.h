#ifndef CONFIG_H
#define CONFIG_H

// --- Wi-Fi Credentials ---
#define WIFI_SSID     "RC-CONTROLLER"
#define WIFI_PASSWORD "RCController123"

// --- UDP Settings ---
#define UDP_PORT      5005

// --- Failsafe Timeout ---
#define FAILSAFE_TIMEOUT_MS 300

// --- GPIO Pin Configuration (L298N Motor Driver - User Preset) ---
// Left Motor Pins (Motor A)
#define MOTOR_LEFT_EN   25  // Speed A (PWM)
#define MOTOR_LEFT_IN1  13  // Direction 1 (en1)
#define MOTOR_LEFT_IN2  12  // Direction 2 (en2)

// Right Motor Pins (Motor B)
#define MOTOR_RIGHT_EN  26  // Speed B (PWM)
#define MOTOR_RIGHT_IN1 14  // Direction 3 (en3)
#define MOTOR_RIGHT_IN2 27  // Direction 4 (en4)


// --- PWM Configuration ---
#define PWM_FREQ         5000
#define PWM_RESOLUTION   8    // 8-bit resolution (0 - 255)
#define PWM_CHANNEL_LEFT  0
#define PWM_CHANNEL_RIGHT 1

// --- Debugging ---
#define SERIAL_BAUD      115200

#endif // CONFIG_H
