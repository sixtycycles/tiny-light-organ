int photocellPin = 0; 
int ID = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(100);

 int photocellReading = analogRead(photocellPin);  
 String obs = String(ID,DEC) + "," + String(photocellReading,DEC); 
 Serial.println(obs);
 
  ID = ID + 1;
  
}
