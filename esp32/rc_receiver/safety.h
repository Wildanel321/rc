#ifndef SAFETY_H
#define SAFETY_H

#include <Arduino.h>
#include "config.h"
#include "motor.h"

void initSafety();
void resetWatchdog();
void updateSafety();
bool isFailsafeActive();

#endif // SAFETY_H
