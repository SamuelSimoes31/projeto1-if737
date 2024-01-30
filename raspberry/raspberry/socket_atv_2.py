import socket
import sys
import RPi.GPIO as GPIO
import time

LED = 3
BUZ = 7


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUZ, GPIO.OUT)

Led = GPIO.PWM(LED, 30)
Led.start(0)
Buzzer = GPIO.PWM(BUZ, .5)
Buzzer.start(50)

led_duty = 0
buz_freq = .5

GPIO.setup(LED,GPIO.OUT)

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mysock.bind(('192.168.0.123',3001))
except socket.error:
    print("Failed to bind")
    sys.exit()
mysock.listen()
try:
    while True:
        conn,addr = mysock.accept()

        data = conn.recv(1000)
        # if not data: break
        # print('Comando raw digitado:', data.decode())
        CMD = data.decode().strip()
        # print('Comando digitado:', CMD)

        message = 'HTTP/1.1 200 OK\nContent-type:text/html\n\n'

        if(CMD.startswith('GET /LH')):
            # conn.sendall(bytes('LIGANDO LED\n','utf-8'))
            if led_duty < 100 :
                led_duty += 10

        elif(CMD.startswith('GET /LL')):
            # conn.sendall(bytes('DESLIGANDO LED\n','utf-8'))
            if led_duty > 0:
                led_duty -= 10

        elif(CMD.startswith('GET /BH')):
            if buz_freq >= 256:
                buz_freq += 10
            else:
                buz_freq *= 2

        elif(CMD.startswith('GET /BL')):
            if buz_freq >= 0.5:
                if buz_freq <= 256:
                    buz_freq /= 2
                else:
                    buz_freq -= 10
        
        
        Led.ChangeDutyCycle(led_duty)

        if (led_duty != 100):
            message += 'Click <a href=\"/LH\">here</a> to turn up the LED\'s brightness.<br>'
    
        if (led_duty != 0):
            message += 'Click <a href=\"/LL\">here</a> to turn down the LED\'s brightness.<br>'
        
        message += '<br>Click <a href=\"/BH\">here</a> to turn up the BUZZER\'s tone.<br>'

        if(buz_freq < 0.5):
            Buzzer.ChangeDutyCycle(0)
        else:
            Buzzer.ChangeFrequency(buz_freq)
            Buzzer.ChangeDutyCycle(50)

            message += 'Click <a href=\"/BL\">here</a> to turn down the BUZZER\'s tone.<br>'

        message += '\n'
        conn.sendall(bytes(message, 'utf-8'))
        
        conn.close()

except KeyboardInterrupt:
    print("Server stopped by User")
    if conn:
        conn.close()
    if mysock:
        mysock.close()
    GPIO.cleanup()