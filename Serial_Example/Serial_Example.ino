//Rod O'Connor for SIE558 final project. 
int pin1 = 0;
int pin2 = 3;
int pin3 = 5; 

void setup() {
  Serial.begin(9600);
}

void loop() {
  
int pin1read = analogRead(pin1);
int pin2read = analogRead(pin2);
int pin3read = analogRead(pin3);

String obs = String(pin1read,DEC) + "," + String(pin2read,DEC)+ ","+String(pin3read,DEC) ; 
Serial.println(obs);  
}
