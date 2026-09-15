#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>
#include "config.h"

void initMotors();
void setLeftMotor(int speed);
void setRightMotor(int speed);
void setMotors(int left, int right);
void stopMotors();

#endif // MOTOR_H
