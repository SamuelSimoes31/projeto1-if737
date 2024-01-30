import socket
import json
import os

os.system('clear')

user = input("Digite seu nome de usuário: ")

os.system('clear')
print(f"Olá, {user}.\n")

while(True):

    print("1. Mudar os temporizadores do semáforo")
    print("2. Visualizar log de mudanças no semáforo")
    print("3. Visualizar log de passagem de carros\n")

    op = int(input("Selecione a operação a ser feita: "))

    os.system('clear')

    if op == 1:
        request = {}
        request['user'] = user
        request['duration'] = []

        request['duration'].append(float(input("Digite a nova duração do sinal verde (s): ")))
        os.system('clear')
        request['duration'].append(float(input("Digite a nova duração do sinal amarelo (s): ")))
        os.system('clear')
        request['duration'].append(float(input("Digite a nova duração do sinal vermelho (s): ")))
        os.system('clear')

        request = 'POST /CFG HTTP/1.1\n\n' + json.dumps(request)

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.connect(('192.168.0.123', 3000))
        mysocket.send(request.encode())

        response = mysocket.recv(1000).decode()
        if not response.startswith('HTTP/1.1 200 OK'):
            print(f"Falha de recepção no servidor: {response[0]}\n")

        mysocket.close()

    elif op == 2:
        request = 'GET /CFG\n\n'

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.connect(('192.168.0.123', 3000))
        mysocket.send(request.encode())

        response = mysocket.recv(1000).decode().strip().split('\n')
        if not response[0].startswith('HTTP/1.1 200 OK'):
            print(f"Falha de recepção no servidor: {response[0]}\n")

        else:
            log_cfg = json.loads(response[-1])

            print("Log de mudanças no semáforo:\n")

            for element in log_cfg:
                print(' ', element['time'], '- Alteração feita por', element['user'])

            input("\nPressione Enter para continuar")

            os.system('clear')

        mysocket.close()

    elif op == 3:
        request = 'GET /CAR\n\n'

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysocket.connect(('192.168.0.123', 3000))
        mysocket.send(request.encode())

        response = mysocket.recv(1000).decode().strip().split('\n')
        if not response[0].startswith('HTTP/1.1 200 OK'):
            print(f"Falha de recepção no servidor: {response[0]}\n")

        else:
            log_cars = json.loads(response[-1])

            print("Log de passagem de carros:\n")
            print(f"  {log_cars['green']} carros passaram no sinal verde")
            print(f"  {log_cars['red']} carros passaram no sinal vermelho")

            input("\nPressione Enter para continuar")

            os.system('clear')

        mysocket.close()
    else:
        print("Código de operação inválida, tente novamente\n\n")
        

