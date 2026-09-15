#include "motor.h"

static void writePwm(uint8_t pin, uint8_t channel, uint32_t duty) {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
    // Arduino-ESP32 Core 3.x API
    ledcWrite(pin, duty);
#else
    // Arduino-ESP32 Core 2.x API
    ledcWrite(channel, duty);
#endif
}

void initMotors() {
    pinMode(MOTOR_LEFT_IN1, OUTPUT);
    pinMode(MOTOR_LEFT_IN2, OUTPUT);
    pinMode(MOTOR_RIGHT_IN1, OUTPUT);
    pinMode(MOTOR_RIGHT_IN2, OUTPUT);

#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
    // Arduino-ESP32 Core 3.x PWM Setup
    ledcAttach(MOTOR_LEFT_EN, PWM_FREQ, PWM_RESOLUTION);
    ledcAttach(MOTOR_RIGHT_EN, PWM_FREQ, PWM_RESOLUTION);
#else
    // Arduino-ESP32 Core 2.x PWM Setup
    ledcSetup(PWM_CHANNEL_LEFT, PWM_FREQ, PWM_RESOLUTION);
    ledcAttachPin(MOTOR_LEFT_EN, PWM_CHANNEL_LEFT);

    ledcSetup(PWM_CHANNEL_RIGHT, PWM_FREQ, PWM_RESOLUTION);
    ledcAttachPin(MOTOR_RIGHT_EN, PWM_CHANNEL_RIGHT);
#endif

    stopMotors();
}

void setLeftMotor(int speed) {
    speed = constrain(speed, -100, 100);
    uint32_t pwm_val = map(abs(speed), 0, 100, 0, 255);

    if (speed > 0) {
        digitalWrite(MOTOR_LEFT_IN1, HIGH);
        digitalWrite(MOTOR_LEFT_IN2, LOW);
    } else if (speed < 0) {
        digitalWrite(MOTOR_LEFT_IN1, LOW);
        digitalWrite(MOTOR_LEFT_IN2, HIGH);
    } else {
        digitalWrite(MOTOR_LEFT_IN1, LOW);
        digitalWrite(MOTOR_LEFT_IN2, LOW);
        pwm_val = 0;
    }

    writePwm(MOTOR_LEFT_EN, PWM_CHANNEL_LEFT, pwm_val);
}

void setRightMotor(int speed) {
    speed = constrain(speed, -100, 100);
    uint32_t pwm_val = map(abs(speed), 0, 100, 0, 255);

    if (speed > 0) {
        digitalWrite(MOTOR_RIGHT_IN1, HIGH);
        digitalWrite(MOTOR_RIGHT_IN2, LOW);
    } else if (speed < 0) {
        digitalWrite(MOTOR_RIGHT_IN1, LOW);
        digitalWrite(MOTOR_RIGHT_IN2, HIGH);
    } else {
        digitalWrite(MOTOR_RIGHT_IN1, LOW);
        digitalWrite(MOTOR_RIGHT_IN2, LOW);
        pwm_val = 0;
    }

    writePwm(MOTOR_RIGHT_EN, PWM_CHANNEL_RIGHT, pwm_val);
}

void setMotors(int left, int right) {
    setLeftMotor(left);
    setRightMotor(right);
}

void stopMotors() {
    digitalWrite(MOTOR_LEFT_IN1, LOW);
    digitalWrite(MOTOR_LEFT_IN2, LOW);
    digitalWrite(MOTOR_RIGHT_IN1, LOW);
    digitalWrite(MOTOR_RIGHT_IN2, LOW);

    writePwm(MOTOR_LEFT_EN, PWM_CHANNEL_LEFT, 0);
    writePwm(MOTOR_RIGHT_EN, PWM_CHANNEL_RIGHT, 0);
}
