/*
 * Note: The modular Wi-Fi RC Controller firmware with UDP receiver,
 * input validation, and active 300 ms failsafe watchdog is located in:
 *   esp32/rc_receiver/rc_receiver.ino
 *
 * Your custom GPIO pin setup has been mapped in esp32/rc_receiver/config.h:
 *   MOTOR_LEFT_EN   (spedA) -> GPIO 25
 *   MOTOR_LEFT_IN1  (en1)   -> GPIO 13
 *   MOTOR_LEFT_IN2  (en2)   -> GPIO 12
 *   MOTOR_RIGHT_EN  (spedB) -> GPIO 26
 *   MOTOR_RIGHT_IN1 (en3)   -> GPIO 14
 *   MOTOR_RIGHT_IN2 (en4)   -> GPIO 27
 */

const int trigPin = 32;
const int echoPin = 33;

const int en1 = 13;
const int en2 = 12;
const int en3 = 14;
const int en4 = 27;
const int spedA = 25;
const int spedB = 26;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(en1, OUTPUT);
  pinMode(en2, OUTPUT);
  pinMode(en3, OUTPUT);
  pinMode(en4, OUTPUT);
  pinMode(spedA, OUTPUT);
  pinMode(spedB, OUTPUT);

  analogWrite(spedA, 225);
  analogWrite(spedB, 225);

  maju();
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;

  Serial.print("Jarak: ");
  Serial.println(distance);
  delay(100);

  if(distance >= 25){
    maju();
  }
  else{
    stop();
    delay(1000);
    mundur();
    delay(1000);
    stop();
    belokkiri();
    delay(1000);
  }
}

void maju(){
 digitalWrite(en1, HIGH);
 digitalWrite(en2, LOW);
 digitalWrite(en3, HIGH);
 digitalWrite(en4, LOW);
}

void mundur(){
 digitalWrite(en1, LOW);
 digitalWrite(en2, HIGH);
 digitalWrite(en3, LOW);
 digitalWrite(en4, HIGH);
}

void belokkanan(){
 digitalWrite(en1, LOW);
 digitalWrite(en2, HIGH);
 digitalWrite(en3, HIGH);
 digitalWrite(en4, LOW);
}

void belokkiri(){
 digitalWrite(en1, HIGH);
 digitalWrite(en2, LOW);
 digitalWrite(en3, LOW);
 digitalWrite(en4, HIGH);
}

void stop(){
 digitalWrite(en1, LOW);
 digitalWrite(en2, LOW);
 digitalWrite(en3, LOW);
 digitalWrite(en4, LOW);
}