import socket as sk
host = '127.0.0.1'
port = 6969
server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind((host,port))
server.listen()
while True:
    com,addr=server.accept()
    print(f"Connected to {addr}")
    message = com.recv(1024).decode('utf-8')
    print(f"message from client is : {message}")
    com.send(f"got ur message Thank you".encode('utf-8'))
    com.close()
    print(f"connection with {addr} ended")
        
print("-----------------all ok------------------")