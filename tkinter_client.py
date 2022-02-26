from email import message
from tkinter import *
import socket
import threading
from tkinter import messagebox


from matplotlib.pyplot import fill


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddr=((socket.gethostname(),9999))


class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Client")
        self.root.geometry("400x400")
        self.name = StringVar()
        self.login = Frame(self.root,height=400,width=400,bg='#00ff00')
        self.login.pack(fill='both',expand=True)

        #crteate label
        self.name_label = Label(self.login,text="Enter your name: ")
        self.name_label.grid(row=0,column=0)
        #create entry
        self.name_entry = Entry(self.login,textvariable=self.name)
        self.name_entry.grid(row=0,column=1)
        #create button
        self.enter_button = Button(self.login,text="Enter",command=self.enter_button_clicked)
        self.enter_button.grid(row=1,column=1)
        self.root.mainloop()

    def send_message(self):
        try:
            s.sendto(self.name_entry.get().encode(),serverAddr)
            s.settimeout(2)
            reply,cIp=s.recvfrom(1024)
            print(reply.decode())
            if reply:

                self.login.destroy()
                print('messsaage sent')
            else:
                print('message not sent')
        except socket.timeout:
            print('timeout')
            messagebox.showinfo('Error','Connection timed out')
            self.root.destroy()
            
    def enter_button_clicked(self):
    
        send_message = threading.Thread(target=self.send_message)
        send_message.start()

app = GUI()
