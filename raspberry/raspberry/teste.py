# from machine import Pin, PWM
import RPi.GPIO as GPIO
# from utime import sleep
import time

BUZ = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZ, GPIO.OUT)

buzzer = GPIO.PWM(BUZ,1)
buzzer.start(50)

tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}
song = [
  'FS5', 'FS5', 'D5', 'B4', 'B4', 'E5', 
  'E5', 'E5', 'GS5', 'GS5', 'A5', 'B5', 
  'A5', 'A5', 'A5', 'E5', 'D5', 'FS5', 
  'FS5', 'FS5', 'E5', 'E5', 'FS5', 'E5'
]

durations = [
  8, 8, 8, 4, 4, 4, 
  4, 5, 8, 8, 8, 8, 
  8, 8, 8, 4, 4, 4, 
  4, 5, 8, 8, 8, 8
]

# song = ["E5","G5","A5","P","E5","G5","B5","A5","P","E5","G5","A5","P","G5","E5"]

def playtone(frequency):
    buzzer.ChangeFrequency(frequency)
    buzzer.ChangeDutyCycle(50)

def bequiet():
    buzzer.ChangeDutyCycle(0)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            # print(tones[mysong[i]])
            playtone(tones[mysong[i]])
        time.sleep(1/durations[i])
        bequiet()
        time.sleep(0.5/durations[i])
    bequiet()

# playtone(2)
# time.sleep(1)
try:
    while(1):
        playsong(song)
except:
    GPIO.cleanup()