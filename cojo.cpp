// INPUTS
#define LED 41
#define BUTTON 39
#define PIR 7

// OUTPUTS
#define BUZZER 43
#define SEG_A 48
#define SEG_B 46
#define SEG_C 49
#define SEG_D 51
#define SEG_E 53
#define SEG_F 50
#define SEG_G 52

// [DÍGITO][SEGMENTO]
byte seven_seg_digits[16][7] = {
  { 1, 1, 1, 1, 1, 1, 0 },  // = Digit 0
  { 0, 1, 1, 0, 0, 0, 0 },  // = Digit 1
  { 1, 1, 0, 1, 1, 0, 1 },  // = Digit 2
  { 1, 1, 1, 1, 0, 0, 1 },  // = Digit 3
  { 0, 1, 1, 0, 0, 1, 1 },  // = Digit 4
  { 1, 0, 1, 1, 0, 1, 1 },  // = Digit 5
  { 1, 0, 1, 1, 1, 1, 1 },  // = Digit 6
  { 1, 1, 1, 0, 0, 0, 0 },  // = Digit 7
  { 1, 1, 1, 1, 1, 1, 1 },  // = Digit 8
  { 1, 1, 1, 0, 0, 1, 1 },  // = Digit 9
  { 1, 1, 1, 0, 1, 1, 1 },  // = Digit A
  { 0, 0, 1, 1, 1, 1, 1 },  // = Digit B
  { 1, 0, 0, 1, 1, 1, 0 },  // = Digit C
  { 0, 1, 1, 1, 1, 0, 1 },  // = Digit D
  { 1, 0, 0, 1, 1, 1, 1 },  // = Digit E
  { 1, 0, 0, 0, 1, 1, 1 }   // = Digit F
};

void printSevenSeg(int digit) {
  digitalWrite(SEG_A, seven_seg_digits[digit][0]);
  digitalWrite(SEG_B, seven_seg_digits[digit][1]);
  digitalWrite(SEG_C, seven_seg_digits[digit][2]);
  digitalWrite(SEG_D, seven_seg_digits[digit][3]);
  digitalWrite(SEG_E, seven_seg_digits[digit][4]);
  digitalWrite(SEG_F, seven_seg_digits[digit][5]);
  digitalWrite(SEG_G, seven_seg_digits[digit][6]);
}

void clearSevenSeg() {
  digitalWrite(SEG_A, LOW);
  digitalWrite(SEG_B, LOW);
  digitalWrite(SEG_C, LOW);
  digitalWrite(SEG_D, LOW);
  digitalWrite(SEG_E, LOW);
  digitalWrite(SEG_F, LOW);
  digitalWrite(SEG_G, LOW);
}


void setupAlarm() {
  for (int i = 0; i < 40; i++) {
    digitalWrite(LED, i % 2);
    delay(250);
  }
  digitalWrite(LED, 0);
}

void activateAlarm() {
  Serial.println("Activate alarm");
  digitalWrite(BUZZER, HIGH);
  delay(100);
  digitalWrite(BUZZER, LOW);
  delay(250);
  digitalWrite(BUZZER, HIGH);
  delay(100);
  digitalWrite(BUZZER, LOW);
}

void waitPassword() {
  String password = "Sugoma";
  int t0 = millis(), tf;
  String sentPassword = "";
  bool triedFlag = false, receivedFlag = false;

  do {
    tf = millis();

    printSevenSeg((10000 - (tf - t0)) / 1000);

    if (receivedFlag || ((tf - t0) > 10000))
      if (!triedFlag) {
        triedFlag = true;
        receivedFlag = false;

        Serial.println("Senha errada ou tempo expirado, você só tem mais uma chance...");

        t0 = tf;

      } else {
        triggerAlarm();
      }

    if (Serial.available()) {
      sentPassword = Serial.readString();
      sentPassword.trim();
      receivedFlag = true;
    }

  } while (sentPassword != password);

  Serial.println("Senha correta");
  clearSevenSeg();
}

void triggerAlarm() {
  bool switchFlag = false;
  while (true) {
    digitalWrite(BUZZER, !switchFlag);
    digitalWrite(LED, switchFlag);
    delay(250);
    switchFlag = !switchFlag;
  }
}

typedef enum {
  DESATIVADO,
  ATIVADO,
  DETECTOU,
} MACHINE_STATE;

MACHINE_STATE state;

void setup() {
  pinMode(SEG_A, OUTPUT);
  pinMode(SEG_B, OUTPUT);
  pinMode(SEG_C, OUTPUT);
  pinMode(SEG_D, OUTPUT);
  pinMode(SEG_E, OUTPUT);
  pinMode(SEG_F, OUTPUT);
  pinMode(SEG_G, OUTPUT);

  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  pinMode(PIR, INPUT);
  pinMode(BUZZER, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  while (digitalRead(BUTTON));
  setupAlarm();

  while (!digitalRead(PIR));
  activateAlarm();

  waitPassword();



  // switcth(state){
  //   case DESATIVADO:
  //       if(!digitalRead(BUTTON)) setupAlarm();
  //       break;
  //   case ATIVADO:
  // }
  // digitalWrite(13, digitalRead(PIR));
}
