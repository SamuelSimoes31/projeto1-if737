import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time

SEG1_A = 3
SEG1_B = 5
SEG1_C = 7
SEG1_D = 11
SEG1_E = 13
SEG1_F = 15
SEG1_G = 19

SEG2_A = 12
SEG2_B = 16
SEG2_C = 18
SEG2_D = 22
SEG2_E = 24
SEG2_F = 26
SEG2_G = 32

# [DÍGITO][SEGMENTO]
seven_seg_digits = [
  [ 1, 1, 1, 1, 1, 1, 0 ],  # Digit 0
  [ 0, 1, 1, 0, 0, 0, 0 ],  # Digit 1
  [ 1, 1, 0, 1, 1, 0, 1 ],  # Digit 2
  [ 1, 1, 1, 1, 0, 0, 1 ],  # Digit 3
  [ 0, 1, 1, 0, 0, 1, 1 ],  # Digit 4
  [ 1, 0, 1, 1, 0, 1, 1 ],  # Digit 5
  [ 1, 0, 1, 1, 1, 1, 1 ],  # Digit 6
  [ 1, 1, 1, 0, 0, 0, 0 ],  # Digit 7
  [ 1, 1, 1, 1, 1, 1, 1 ],  # Digit 8
  [ 1, 1, 1, 0, 0, 1, 1 ],  # Digit 9
  [ 1, 1, 1, 0, 1, 1, 1 ],  # Digit A
  [ 0, 0, 1, 1, 1, 1, 1 ],  # Digit B
  [ 1, 0, 0, 1, 1, 1, 0 ],  # Digit C
  [ 0, 1, 1, 1, 1, 0, 1 ],  # Digit D
  [ 1, 0, 0, 1, 1, 1, 1 ],  # Digit E
  [ 1, 0, 0, 0, 1, 1, 1 ]   # Digit F
]

GPIO.setup(SEG1_A, GPIO.OUT)
GPIO.setup(SEG1_B, GPIO.OUT)
GPIO.setup(SEG1_C, GPIO.OUT)
GPIO.setup(SEG1_D, GPIO.OUT)
GPIO.setup(SEG1_E, GPIO.OUT)
GPIO.setup(SEG1_F, GPIO.OUT)
GPIO.setup(SEG1_G, GPIO.OUT)

GPIO.setup(SEG2_A, GPIO.OUT)
GPIO.setup(SEG2_B, GPIO.OUT)
GPIO.setup(SEG2_C, GPIO.OUT)
GPIO.setup(SEG2_D, GPIO.OUT)
GPIO.setup(SEG2_E, GPIO.OUT)
GPIO.setup(SEG2_F, GPIO.OUT)
GPIO.setup(SEG2_G, GPIO.OUT)

def printSevenSeg2(digit):
    GPIO.output(SEG1_A, seven_seg_digits[digit][0])
    GPIO.output(SEG1_B, seven_seg_digits[digit][1])
    GPIO.output(SEG1_C, seven_seg_digits[digit][2])
    GPIO.output(SEG1_D, seven_seg_digits[digit][3])
    GPIO.output(SEG1_E, seven_seg_digits[digit][4])
    GPIO.output(SEG1_F, seven_seg_digits[digit][5])
    GPIO.output(SEG1_G, seven_seg_digits[digit][6])

def printSevenSeg1(digit):
    GPIO.output(SEG2_A, seven_seg_digits[digit][0])
    GPIO.output(SEG2_B, seven_seg_digits[digit][1])
    GPIO.output(SEG2_C, seven_seg_digits[digit][2])
    GPIO.output(SEG2_D, seven_seg_digits[digit][3])
    GPIO.output(SEG2_E, seven_seg_digits[digit][4])
    GPIO.output(SEG2_F, seven_seg_digits[digit][5])
    GPIO.output(SEG2_G, seven_seg_digits[digit][6])


try:
    a = 0
    while True:
        printSevenSeg1(a)
        printSevenSeg2(a)
        time.sleep(1)
        a = (a + 1)%16

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()

