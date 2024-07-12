import threading as th
import socket as sk

enc='utf-8' #encoding format
host = '127.0.0.1' #localhost
port = 50505
server= sk.socket(sk.AF_INET,sk.SOCK_STREAM)
try:
    server.bind((host,port))
except OSError:
    print("Another instance of server already running")
    exit()
server.listen()
clients=[]
usernames=[]
# for broadcasting messages to all users
def broadcast(message):
    for client in clients:
        client.send(message.encode(enc))
# for handling client along with recieving and broadcasting message
def handle(client):
    while True:
        try:
            message=client.recv(1024).decode(enc)
            broadcast(message)
        except ConnectionResetError:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            username=usernames[index]
            broadcast(f"{username} has disconnected")
            usernames.remove(username)
            break
#receive messages and adding users
def recieve():
    while True:
        client,addr = server.accept()
        print(f"Connected with Address:{addr}")
        client.send("UNAME".encode(enc))
        username=client.recv(1024).decode(enc)
        usernames.append(username)
        clients.append(client)
        print(f"{username} has connected")
        broadcast(f"{username} has joined the chat")
        client.send("Connected to the server".encode(enc))
        handle_thread = th.Thread(target=handle,args=(client,))
        handle_thread.start()
print("Server is listening........")
recieve()
