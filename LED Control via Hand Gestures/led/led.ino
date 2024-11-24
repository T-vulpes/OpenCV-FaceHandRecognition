const int ledPin = 8; // LED'in bağlı olduğu pin

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600); // Seri haberleşmeyi başlat
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(ledPin, HIGH); // LED'i yak
    } else if (command == '0') {
      digitalWrite(ledPin, LOW); // LED'i söndür
    }
  }
}
