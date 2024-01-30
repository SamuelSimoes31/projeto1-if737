import socket
import sys
import RPi.GPIO as GPIO
import time

LED = 3
CAP = 5
BUZ = 7


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUZ, GPIO.OUT)
GPIO.setup(CAP, GPIO.OUT)
Buzzer = GPIO.PWM(BUZ, 1)
Buzzer.start(0)
buz_duration = 0

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


# -------------------


mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mysock.bind(('127.0.0.1',3000))
except socket.error:
    print("Failed to bind")
    sys.exit()
mysock.listen()
try:
    conn,addr = mysock.accept()
    while True:
        data = conn.recv(1000)
        if not data: break
        CMD = data.decode().strip()
        print('Comando digitado:', CMD)

        if(CMD == 'LED ON'):
            conn.sendall(bytes('LIGANDO LED\n','utf-8'))
            GPIO.output(LED,1)
        if(CMD == 'LED OFF'):
            conn.sendall(bytes('DESLIGANDO LED\n','utf-8'))
            GPIO.output(LED,0)
        if(CMD == 'LDR'):
            valor = leituraAnalogica()
            conn.sendall(bytes(f'VALOR LDR: {valor}s\n','utf-8'))
        if(CMD.split()[0] == 'BUZZER'):
            try:
                freq = int(CMD.split()[1])
                dura = int(CMD.split()[2])
                buz_duration = dura
                Buzzer.ChangeFrequency(freq)
                Buzzer.ChangeDutyCycle(50)
                
                conn.sendall(bytes('TOCANDO BUZZER\n','utf-8'))

                time.sleep(dura)
                Buzzer.ChangeDutyCycle(0)
                conn.sendall(bytes('ACABOU\n','utf-8'))
            except:
                pass

except KeyboardInterrupt:
    print("Server stopped by User")
    # conn.close()
    mysock.close()
    GPIO.cleanup()