import tkinter
import tkinter.scrolledtext
from blues import *
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
                print("Server disconnected")
                client.close()
                exit()
                break
def write():
    message = f"{username}: {input_area.get('1.0','end')}"
    client.send(message.encode(enc))
    input_area.delete("1.0",'end')

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
send_button=tkinter.Button(root,text="Send",fg=blue2,bg=blue4,width=60,height=62,
                           font=("Arial",12),activeforeground=blue4,activebackground=blue3,
                           image=send_icon,compound="top",
                           command=write)
send_button.place(x=900,y=600)
receive_thread = th.Thread(target=receive)
receive_thread.start()
root.mainloop()