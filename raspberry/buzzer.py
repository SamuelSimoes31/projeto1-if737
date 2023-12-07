import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time

BUZZER_PIO = 29
GPIO.setup(BUZZER_PIO, GPIO.OUT)
BUZZER = GPIO.PWM(BUZZER_PIO, 1)
BUZZER.start(50)

try:
    a = 0
    while True:
        BUZZER.ChangeFrequency(a)
        time.sleep(1)
        a += 1
        a %= 2
        
        print(a)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()