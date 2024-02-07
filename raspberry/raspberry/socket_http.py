import socket
import sys
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mysock.bind(('127.0.0.1',3700))
except socket.error:
    print("Failed to bind")
    sys.exit()
mysock.listen()
while True:
    conn,addr = mysock.accept()
    data = conn.recv(1000)
    if not data: break
    message = "HTTP/1.0 200 OK\n\n<h1>Hello World</h1>"
    conn.sendall(bytes(message,"utf-8"))
conn.close()
mysock.close()