import RPi.GPIO as GPIO
import time
from numpy import interp
GPIO.setmode(GPIO.BOARD)

LED = 12
CAP = 3
GPIO.setup(CAP,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)

def descarga ():
    GPIO.setup(CAP,GPIO.OUT)
    GPIO.output(CAP,GPIO.LOW)
    time.sleep(0.15)

def carga():
    GPIO.setup(CAP,GPIO.IN)
    tempoInicial = time.time_ns()
    while (GPIO.input(CAP) == GPIO.LOW):
        pass
    tempoFinal = time.time_ns() - tempoInicial 
    time.sleep(.01)
    return tempoFinal/1e6

def leituraAnalogica():
    descarga()
    return carga()

maximus = 0
minimus = 1

pwm = GPIO.PWM(LED,100)
pwm.start(0)
while True:
    valor = leituraAnalogica()
    maximus = max(valor,maximus)
    minimus = min(valor,minimus)
    valorPWM = interp(valor,[minimus,maximus],[0,100])
    print(f"valor: {valor}")
    print(f"max:{maximus}, min: {minimus}")
    print(f"valorPWM: {valorPWM}")
    pwm.ChangeDutyCycle(valorPWM)
    
    
