from math import ceil
import socket
import sys
import RPi.GPIO as GPIO
import time
import json
import select

LED_GREEN = 3
LED_YELLOW = 5
LED_RED = 7

PIR = 11

SEG_A = 12
SEG_B = 16
SEG_C = 18
SEG_D = 22
SEG_E = 24
SEG_F = 26
SEG_G = 32

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIR,GPIO.IN)
GPIO.setup(LED_GREEN,GPIO.OUT)
GPIO.setup(LED_YELLOW,GPIO.OUT)
GPIO.setup(LED_RED,GPIO.OUT)

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

GPIO.setup(SEG_A, GPIO.OUT)
GPIO.setup(SEG_B, GPIO.OUT)
GPIO.setup(SEG_C, GPIO.OUT)
GPIO.setup(SEG_D, GPIO.OUT)
GPIO.setup(SEG_E, GPIO.OUT)
GPIO.setup(SEG_F, GPIO.OUT)
GPIO.setup(SEG_G, GPIO.OUT)

def printSevenSeg(digit):
    for idx, seg in enumerate([SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G]):
        GPIO.output(seg, seven_seg_digits[digit][idx])

def clearSevenSeg():
    for seg in [SEG_A, SEG_B, SEG_C, SEG_D, SEG_E, SEG_F, SEG_G]:
        GPIO.output(seg, 0)

semaforo = 0

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# LOGS
cfg_file = open("log_cfg", "a+")
cars_file = open("log_cars", "r+")

cars_file.seek(0)
if not cars_file.read(1):
    cars_file.write(
        json.dumps({'green' : 0, 
                    'red'   : 0}))

# SEMAFORO
ref_time = time.time()

duration = [4, 2, 4]

# DETECÇÃO
last_detected = False

try:
    mysock.bind(('192.168.0.123',3000))
except socket.error:
    print("Failed to bind")
    sys.exit()
mysock.listen()
try:
    while True:

        available, _, _ = select.select([mysock], [], [], 0.1)

        if not available:

            cur_time = time.time()

            if (cur_time - ref_time) > duration[semaforo]:
                semaforo = (semaforo + 1) % 3

                ref_time = cur_time

            if(semaforo == 0):
                printSevenSeg(ceil(duration[semaforo] - (cur_time - ref_time))-1)
            else:
                clearSevenSeg()

            GPIO.output(LED_GREEN, semaforo == 0)
            GPIO.output(LED_YELLOW, semaforo == 1)
            GPIO.output(LED_RED, semaforo == 2)


            detected = GPIO.input(PIR)

            if not last_detected and detected:
                cars_file.seek(0)
                log_cars = json.loads(cars_file.read())

                if semaforo == 2:
                    log_cars['red'] += 1
                else:
                    log_cars['green'] += 1

                cars_file.truncate(0)
                cars_file.seek(0)
                cars_file.write(json.dumps(log_cars))

            last_detected = detected

        else:

            conn,addr = available[0].accept()

            data = conn.recv(1000)
            
            CMD = data.decode().strip().split('\n')
            print('Comando digitado:', CMD)

            message = 'HTTP/1.1 200 OK\n\n'

            if(CMD[0].startswith('POST /CFG')):
                body = json.loads(CMD[-1])

                duration = body['duration']
                
                body.pop('duration')
                body['time'] = time.asctime()

                if body['user'] and body['time']:
                    # log_cfg.append(body)
                    cfg_file.write(json.dumps(body) + '\n')
                else:
                    print("Failed to log configuration request\n")

            elif(CMD[0].startswith('GET /CFG')):
                cfg_file.seek(0)
                response = [json.loads(line) for line in cfg_file][-10:]

                message += json.dumps(response)

            elif(CMD[0].startswith('GET /CAR')):
                cars_file.seek(0)
                message += cars_file.read()
            
            message += '\n'
            conn.sendall(bytes(message, 'utf-8'))
            
            conn.close()

except KeyboardInterrupt:
    print("Server stopped by User")
    if conn:
        conn.close()
    if mysock:
        mysock.close()
    cars_file.close()
    cfg_file.close()

    GPIO.cleanup()