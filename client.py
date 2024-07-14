import tkinter
import tkinter.scrolledtext
from blues import *
import threading as th
import socket as sk

enc='utf-8'
host = ""
port = 50505
username = ""
client= sk.socket(sk.AF_INET,sk.SOCK_STREAM)

def join():
    global host,username 
    host = server_entry.get()
    username = uname_entry.get()
    try:
        client.connect((host,port))
    except:
        connect.destroy()
        sd = tkinter.Tk()
        sd.geometry("400x200")
        sd.resizable(False,False)
        sd.config(background=blue2)
        sd.title("Error")
        appicon = tkinter.PhotoImage(file="images\\appicon.png")
        sd.iconphoto(True,appicon)
        disconnect_icon = tkinter.PhotoImage(file="images\\disconnected_resized.png")
        disconnected=tkinter.Label(sd,text="Server refused to connect",fg=blue5,bg=blue2,font=("Arial",15),image=disconnect_icon,compound="left")
        disconnected.place(x=80,y=80)
        sd.protocol("WM_DELETE_WINDOW",exit)
        sd.mainloop()
    connect.destroy()
connect = tkinter.Tk()
connect.geometry("500x300")
connect.resizable(False, False)
connect.title("Connect to chatroom")
connect.config(background=blue2)
appicon = tkinter.PhotoImage(file="images\\appicon.png")
connect.iconphoto(True,appicon)
server_entry = tkinter.Entry(connect,font=("Arial",15))
server_entry.place(x=150,y=70)
uname_entry = tkinter.Entry(connect,font=("Arial",15))
uname_entry.place(x=150,y=130)
connect_label=tkinter.Label(connect,text="Enter Server IP and Username",fg=blue5,bg=blue2,font=("Arial",15))
connect_label.pack(padx=10,pady=10)
server_icon=tkinter.PhotoImage(file="images\\server_resized.png")
server_label=tkinter.Label(connect,bg=blue2,image=server_icon)
server_label.place(x=90,y=60)
user_icon=tkinter.PhotoImage(file="images\\user_resized.png")
user_label=tkinter.Label(connect,bg=blue2,image=user_icon)
user_label.place(x=90,y=120)
connect_icon=tkinter.PhotoImage(file="images\\join_resized.png")
connect_button=tkinter.Button(connect,fg=blue2,bg=blue4,width=50,height=50,
                            activeforeground=blue4,activebackground=blue3,
                            image=connect_icon,compound="top",
                            command=join)
connect_button.place(x=150,y=200)
exit_icon=tkinter.PhotoImage(file="images\\exit_resized.png")
exit_button=tkinter.Button(connect,fg=blue2,bg=blue4,width=50,height=50,
                            activeforeground=blue4,activebackground=blue3,
                            image=exit_icon,compound="top",
                            command=exit)
exit_button.place(x=300,y=200)
connect.mainloop()

def receive():
    while True:
        try:
            message=client.recv(1024).decode(enc)
            if message=="UNAME":
                client.send(username.encode(enc))
            else:
                chat_display.config(state="normal")
                chat_display.insert('end',message)
                chat_display.yview('end')
                chat_display.config(state='disabled')
        except:
                chat_display.config(state="normal")
                chat_display.insert('end',"Connection closed")
                chat_display.yview('end')
                chat_display.config(state='disabled')
                client.close()
                send_button.config(state="disabled")
                break
def write():
    message = f"{username}: {input_area.get('1.0','end')}"
    client.send(message.encode(enc))
    input_area.delete("1.0",'end')
def stop():
    client.close()
    root.destroy()
root = tkinter.Tk()
root.geometry("1000x700")
root.title("pChatroom")
appicon = tkinter.PhotoImage(file="images\\appicon.png")
root.iconphoto(True,appicon)
root.config(background=blue2)
root.resizable(False, False)
chat_icon=tkinter.PhotoImage(file="images\\chat_resized.png")
chat_label=tkinter.Label(root,text="Chats",fg=blue5,bg=blue2,
                         font=("Arial",12),image=chat_icon,compound="left")
chat_label.place(x=20,y=10)
app_label=tkinter.Label(root,text="pChatroom",fg=blue5,bg=blue2,font=("Arial",25,"bold"))
app_label.pack(padx=10,pady=10)
chat_display= tkinter.scrolledtext.ScrolledText(root,bg=blue1,wrap=tkinter.WORD,state="disabled",height=27,width=80)
chat_display.place(x=20,y=100)
mail_icon=tkinter.PhotoImage(file="images\\email_resized.png")
msg_label=tkinter.Label(root,text="Message",fg=blue5,bg=blue2,
                        font=("Arial",12),image=mail_icon,compound="left")
msg_label.place(x=20,y=550)
input_area=tkinter.Text(root,bg=blue1,width=78,height=3,font=("Arial",14))
input_area.place(x=20,y=600)
send_icon=tkinter.PhotoImage(file="images\\send_resized.png")
send_button=tkinter.Button(root,text="Send",fg=blue2,bg=blue4,width=60,height=60,
                           font=("Arial",12),activeforeground=blue4,activebackground=blue3,
                           image=send_icon,command=write)
send_button.place(x=900,y=600)
exit_icon=tkinter.PhotoImage(file="images\\exit_resized.png")
exit_button=tkinter.Button(root,fg=blue2,bg=blue4,width=50,height=50,
                            activeforeground=blue4,activebackground=blue3,
                            image=exit_icon,command=stop)
exit_button.place(x=900,y=500)
root.protocol("WM_DELETE_WINDOW",exit)
receive_thread = th.Thread(target=receive)
receive_thread.start()
root.mainloop()