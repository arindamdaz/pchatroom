import threading as th
import socket as sk

enc='utf-8'
host = '127.0.0.1'
port = 50505
username=input("Enter your username: ")
client= sk.socket(sk.AF_INET,sk.SOCK_STREAM)
try:
    client.connect((host,port))
except ConnectionRefusedError:
    print("Server is unreachable")
    print("Exiting.....")
    exit()
#for receiving broadcasted message
def receive():
    while True:
        try:
            message=client.recv(1024).decode(enc)
            if message=="UNAME":
                client.send(username.encode(enc))
            else:
                print(message)
        except:
            print("Server disconnected")
            client.close()
            exit()
            break
#sending message to client
def write():
    while True:
        message=f'{username}: {input("")}'
        client.send(message.encode(enc))
#simultaneously running receive and write
receive_thread = th.Thread(target=receive)
receive_thread.start()
write_thread = th.Thread(target=write)
write_thread.start()