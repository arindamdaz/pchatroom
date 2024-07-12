import socket as sk
host = '127.0.0.1'
port = 6969
socket = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
socket.connect((host,port))
socket.send("hello world!".encode('utf-8'))
print(socket.recv(1024).decode('utf-8'))
