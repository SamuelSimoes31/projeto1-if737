// Program: Increasing counter 0 to F
// Modifications and comments: Arduino and Co.
// Based on the program:
// Arduino 7 segment display example software
// http://www.hacktronics.com/Tutorials/arduino-and-7-segment-led.html
// License: http://www.opensource.org/licenses/mit-license.php (Go crazy)
// Defines the connection order of the segments, from digits 0 to F
// This pattern is for common cathode display
// For common anode display, change the values ​​from 0 to 1 and
// from 1 to 0
// 1 = LED on, 0 = LED off, in this order:
// Arduino pins: 2,3,4,5,6,7,8
byte seven_seg_digits [ 16 ][ 7 ] = { { 1,1,1,1,1,1,0 } ,   // = Digit 0 
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
                                 { 1,0,0,0,1,1,1 } // = Digit F   
                                 } ;
void setup ()  
{  
  pinMode ( 2, OUTPUT ) ; //Arduino pin 2 connected to segment A  
  pinMode ( 3, OUTPUT ) ; //Arduino pin 3 connected to segment B
  pinMode ( 4, OUTPUT ) ; //Pin 4 of the Arduino connected to the C segment
  pinMode ( 5, OUTPUT ) ; //Arduino pin 5 connected to segment D
  pinMode ( 6, OUTPUT ) ; //Arduino pin 6 connected to segment E
  pinMode ( 7, OUTPUT ) ; //Pin 7 of the Arduino connected to the F segment
  pinMode ( 8, OUTPUT ) ; //Arduino pin 8 connected to segment G
  pinMode ( 9, OUTPUT ) ; //Pin 9 of the Arduino connected to the POINT segment
  writePoint ( 0 ) ;  // Start with point off
}
void writePoint ( byte dot ) //Function that activates the point on the display    
{  
  digitalWrite ( 9, dot ) ;
}
void sevenSegWrite ( byte digit ) //Function that activates the display   
{
  byte pin = 2;
  //Traverse the array connecting the segments corresponding to the digit
  for ( byte segCount = 0; segCount < 7; ++segCount )   
  { 
    digitalWrite ( pin, seven_seg_digits [ digit ][ segCount ]) ;
    ++pin;
  }
    writePoint ( 1 ) ;  //Connect the point
    delay ( 100 ) ;   //Wait 100 milliseconds
    writePoint ( 0 ) ;  //Turn off the point
}
void loop ()  
{
  //Counter from 0 to 15, connecting the corresponding segments
  //0 to 9 = connects the segments corresponding to numbers
  //10 to 15 = Forms the letters A,B,C,D,E,F
  for ( byte count = 0; count < 16; count++ ) 
  {
     delay ( 500 ) ;
     sevenSegWrite ( count ) ;
  }
  delay ( 4000 ) ;
}