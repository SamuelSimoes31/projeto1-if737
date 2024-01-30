import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time
from numpy import interp

##### 7SEG #####

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

##### ULTRASONIC #####

GPIO_TRIGGER = 21
GPIO_ECHO = 23
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    distance = (TimeElapsed * 34300) / 2
    return distance

##### BUZZER #####

BUZZER_PIO = 29
GPIO.setup(BUZZER_PIO, GPIO.OUT)
Buzzer = GPIO.PWM(BUZZER_PIO, 1)
Buzzer.start(50)

##### LEDS #####

LED_VERDE = 31
LED_AMARELO = 33
LED_VERMELHO = 35

GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_AMARELO, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)

def set_semaforo(verde, amarelo, vermelho):

    GPIO.output(LED_VERDE, verde)
    GPIO.output(LED_AMARELO, amarelo)
    GPIO.output(LED_VERMELHO, vermelho)

    return

# set_semaforo(1,1,1)

##### MAIN #####

UPPER_BOUND = 50.
LOWER_BOUND = 10.
COLLISION_BOUND = 3.

try:
    while True:
        
        dist = distance()

        if dist > 99.: dist = 99.

        printSevenSeg2(int(dist%10))
        printSevenSeg1(int(dist/10))
        
        if dist > UPPER_BOUND :
            Buzzer.ChangeDutyCycle(0)
            set_semaforo(1, 0, 0)

        else:
            Buzzer.ChangeDutyCycle(50)
            Buzzer.ChangeFrequency(int(interp(dist, [LOWER_BOUND, UPPER_BOUND], [10, 3]) ))

            if dist < COLLISION_BOUND:
                Buzzer.ChangeDutyCycle(100)
                flag = 0
                while True:
                    set_semaforo(flag, flag, flag)
                    flag = not flag
                    time.sleep(0.2)


            elif dist < LOWER_BOUND:
                set_semaforo(0, 0, 1)

            else:
                set_semaforo(0, 1, 0)

            
            # set_semaforo (0, 1, 0)

        print(dist)

        time.sleep(0.1)


except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()