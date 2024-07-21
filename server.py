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
ips=[]
banip=[]
def ban(user):
    if user == usernames[0]:
        clients[0].send("You are the admin\n".encode(enc))
    else:
        if user not in usernames:
            clients[0].send(f"{user} not found in chatroom\n".encode(enc))
        else:
            index=usernames.index(user)
            client=clients[index]
            client.send(f"You have been banned by admin\n".encode(enc))
            clients.remove(client)
            client.close()
            broadcast(f"{user} has been banned by admin\n")
            print(f"{user} has been banned by admin")
            usernames.remove(user)
            ip = ips[index]
            banip.append(ip)
            ips.remove(ip)
def kick(user):
    if user == usernames[0]:
        clients[0].send("You are the admin\n".encode(enc))
    else:
        if user not in usernames:
            clients[0].send(f"{user} not found in chatroom\n".encode(enc))
        else:
            index=usernames.index(user)
            client=clients[index]
            client.send(f"You have been kicked out by admin\n".encode(enc))
            clients.remove(client)
            client.close()
            broadcast(f"{user} has been kicked out by admin\n")
            print(f"{user} has been kicked out by admin")
            usernames.remove(user)
# for broadcasting messages to all users
def broadcast(message):
    for client in clients:
        client.send(message.encode(enc))
# for handling client along with recieving and broadcasting message
def handle(client):
    while True:
        try:
            message=client.recv(1024).decode(enc)
            if message[0:6]=="//kick":
                user=message[6:]
                kick(user)
            elif message[0:5]=="//ban":
                user=message[5:]
                ban(user)
            else:
                broadcast(message)
        except ConnectionResetError:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            username=usernames[index]
            broadcast(f"{username} has disconnected\n")
            print(f"{username} has disconnected")
            usernames.remove(username)
            if index==0 and len(clients)>0:
                clients[0].send("ADMIN".encode(enc))
                print(f"{usernames[0]} is admin now")
                #broadcast(f"{username[0]} is admin now\n")    
            break
        except ConnectionAbortedError:
            break
#receive messages and adding users
def recieve():
    while True:
        client,addr = server.accept()
        print(f"Connected with Address:{addr}")
        client.send("UNAME".encode(enc))
        username=client.recv(1024).decode(enc)
        if addr[0] in banip:
            print(f"Banned address {addr} trying to connect with username:{username}")
            client.send(f"BAN".encode(enc))
            client.close()
            continue
        usernames.append(username)
        clients.append(client)
        ips.append(addr[0])
        print(f"{username} has connected")
        broadcast(f"{username} has joined the chat\n")
        client.send("Connected to the server\n".encode(enc))
        if len(clients)==2:
            clients[0].send("ADMIN".encode(enc))
        handle_thread = th.Thread(target=handle,args=(client,))
        handle_thread.start()
print(f"Enter {host} in client to connect")
print("Server is listening........")
recieve()