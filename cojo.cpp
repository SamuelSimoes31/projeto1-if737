// INPUTS
#define LED 47
#define BUTTON 44
#define PIR 7

// OUTPUTS
#define BUZZER 9
#define SEG_A 48
#define SEG_B 46
#define SEG_C 49
#define SEG_D 51
#define SEG_E 53
#define SEG_F 50
#define SEG_G 52

// [DÍGITO][SEGMENTO]
byte seven_seg_digits [ 16 ][ 7 ] = { 
                                    { 1,1,1,1,1,1,0 } ,   // = Digit 0 
                                    { 0,1,1,0,0,0,0 } ,   // = Digit 1
                                    { 1,1,0,1,1,0,1 } ,   // = Digit 2
                                    { 1,1,1,1,0,0,1 } ,   // = Digit 3
                                    { 0,1,1,0,0,1,1 } ,   // = Digit 4
                                    { 1,0,1,1,0,1,1 } ,   // = Digit 5
                                    { 1,0,1,1,1,1,1 } ,   // = Digit 6
                                    { 1,1,1,0,0,0,0 } ,   // = Digit 7
                                    { 1,1,1,1,1,1,1 } ,   // = Digit 8
                                    { 1,1,1,0,0,1,1 } ,   // = Digit 9
                                    { 1,1,1,0,1,1,1 } ,   // = Digit A
                                    { 0,0,1,1,1,1,1 } ,   // = Digit B
                                    { 1,0,0,1,1,1,0 } ,   // = Digit C
                                    { 0,1,1,1,1,0,1 } ,   // = Digit D
                                    { 1,0,0,1,1,1,1 } ,   // = Digit E
                                    { 1,0,0,0,1,1,1 }     // = Digit F   
                                    } ;

void printSevenSeg(int digit){
  digitalWrite(SEG_A,seven_seg_digits[digit][0]);
  digitalWrite(SEG_B,seven_seg_digits[digit][1]);
  digitalWrite(SEG_C,seven_seg_digits[digit][2]);
  digitalWrite(SEG_D,seven_seg_digits[digit][3]);
  digitalWrite(SEG_E,seven_seg_digits[digit][4]);
  digitalWrite(SEG_F,seven_seg_digits[digit][5]);
  digitalWrite(SEG_G,seven_seg_digits[digit][6]);
}


void activateAlarm(){
  for(int i=0; i<40; i++){
    digitalWrite(LED, i%2);
    delay(250);
  }
  digitalWrite(LED, 0);
}

typedef enum {
  DESATIVADO,
  ATIVADO,
  DETECTOU,
} MACHINE_STATE;

MACHINE_STATE state;

void setup()
{
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
}

void loop()
{
  // if(!digitalRead(BUTTON)){
  //   activateAlarm();
  // }
  // switcth(state){
  //   case DESATIVADO:
  //       if(!digitalRead(BUTTON)) activateAlarm();
  //       break;
  //   case ATIVADO: 
  // }
  digitalWrite(13, digitalRead(PIR));
}
