#include <Servo.h>

Servo myServo;  // Servo motor nesnesi
int servoPin = 9;  // Servo motor pini

void setup() {
  Serial.begin(9600);  // Seri port iletişimi başlat
  myServo.attach(servoPin);  // Servo motoru belirtilen pine bağla
  myServo.write(90);  // Başlangıç pozisyonu (orta nokta)
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
