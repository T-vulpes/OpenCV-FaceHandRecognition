#include <Servo.h>

Servo myServo; 
int servoPin = 9;  

void setup() {
  Serial.begin(9600);   #baudrate
  myServo.attach(servoPin);  
  myServo.write(90); 
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  // Komut oku
    command.trim();  // Fazla boşlukları kaldır

    if (command == "RIGHT") {
      myServo.write(180);  // Servo motoru sağa döndür
    } else if (command == "LEFT") {
      myServo.write(0);  // Servo motoru sola döndür
    }
    
  }
}
