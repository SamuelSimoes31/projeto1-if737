import RPi.GPIO as GPIO
import time
#GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    GPIO.output(8,True)
    value = GPIO.input(10)

    if value == False:
        time.sleep(0.1)
        GPIO.output(8,False)
        time.sleep(0.1)