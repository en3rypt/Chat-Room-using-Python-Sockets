from tkinter import *
import socket
import threading
from tkinter import messagebox
from db import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddr=((socket.gethostname(),9999))

class APP:
    def __init__(self):
        self.root = Tk()
        self.root.title("Chat room")
        self.name = StringVar()
        self.msg = StringVar()

        self.username = StringVar()
        self.password = StringVar()


        self.main_page = Frame(self.root)
        self.main_page.pack(fill='both',expand=True)
        self.welcome_label1 = Label(self.main_page,text="Welcome to the chat room",font=("Helvetica",16))
        self.welcome_label1.pack(pady=10)
        self.enter_button = Button(self.main_page,text="Login",font=("Helvetica",12),command=self.login_user)
        self.enter_button.pack()
        self.enter_button = Button(self.main_page,text="Register",font=("Helvetica",12),command=self.register_user)
        self.enter_button.pack()

        self.mainpage = Frame(self.root)
        


        self.l1 = Label(self.mainpage,text='')
        self.l1.pack()

        self.frame = Frame(self.mainpage)
        self.frame.pack()

        self.textbox = Text(self.frame,height=22,width=47)
        self.textbox.pack(side='left')

        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side='right',fill='y')
        

        self.scrollbar.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.textbox.config(state=DISABLED)

        self.frame2 = Frame(self.mainpage)
        self.frame2.pack()

        self.input_left = Entry(self.frame2,textvariable=self.msg,width=35,font=17)
        self.input_left.pack(side='left')
        self.button_right = Button(self.frame2,text='Send',font=17,command=self.send_message)
        self.button_right.pack(side='right')

        self.exit_button = Button(self.mainpage,text='Exit',font=17,command=self.logout)
        self.exit_button.pack()

        

        #LOGIN USER
        self.login = Frame(self.root)

        self.welcome_label3 = Label(self.login,text="Login",font=("Helvetica",16))
        self.welcome_label3.pack(pady=10)

        self.lusrlabel = Label(self.login,text="Enter your username: ",font=("Helvetica",12))
        self.lusrlabel.pack()
        
        self.lusentry = Entry(self.login,textvariable=self.username,font=("Helvetica",12))
        self.lusentry.pack()
        
        self.lpwdlabel = Label(self.login,text="Enter your password: ",font=("Helvetica",12))
        self.lpwdlabel.pack()

        self.lpwdentry = Entry(self.login,show="*",textvariable=self.password,font=("Helvetica",12))
        self.lpwdentry.pack()

        self.lsubmit_button = Button(self.login,text="Submit",font=("Helvetica",12),command=self.validate_login)
        self.lsubmit_button.pack()
        self.back_button = Button(self.login,text="Back",font=("Helvetica",12),command=lambda: self.back(self.login))
        self.back_button.pack()


        #REGISTER USER

        self.register = Frame(self.root)


        self.welcome_label2 = Label(self.register,text="Registration",font=("Helvetica",16))
        self.welcome_label2.pack(pady=10)

        self.rusrlabel = Label(self.register,text="Enter your username: ",font=("Helvetica",12))
        self.rusrlabel.pack()
        
        self.rusentry = Entry(self.register,textvariable=self.username,font=("Helvetica",12))
        self.rusentry.pack()
        
        self.rpwdlabel = Label(self.register,text="Enter your password: ",font=("Helvetica",12))
        self.rpwdlabel.pack()

        self.rpwdentry = Entry(self.register,show="*",textvariable=self.password,font=("Helvetica",12))
        self.rpwdentry.pack()

        self.submit_button = Button(self.register,text="Submit",font=("Helvetica",12),command=self.validate_register)
        self.submit_button.pack()
        self.back_button = Button(self.register,text="Back",font=("Helvetica",12),command=lambda: self.back(self.register))
        self.back_button.pack()

        self.root.mainloop()

    def back(self,frame):
        frame.pack_forget()
        self.main_page.pack()
        
    def register_user(self):
        self.main_page.pack_forget()
        self.register.pack(fill='both',expand=True)

    def login_user(self):
        self.main_page.pack_forget()
        self.login.pack(fill='both',expand=True)
    

    def validate_register(self):
        username = self.username.get()
        password = self.password.get()
        if username == '' or password == '':
           messagebox.showinfo('Error','Please enter all the fields')
        else:
            if ADD_USER(username,password):
                messagebox.showinfo('Success','User registered successfully')
                self.username.set('')
                self.password.set('')
            else:
                messagebox.showinfo('Error','User already exists')
                self.username.set('')
                self.password.set('')

        

    def logout(self):
        s.sendto(f'exit:{self.name.get()} Left the chat'.encode(),serverAddr)
        self.root.destroy()
        sys.exit()


    def send_message(self):
        message = self.msg.get()
        s.sendto(f'send:{message}'.encode(),serverAddr)
        storeMessaage(self.username.get(),message)
        self.input_left.delete(0,END)
            
    def get_message(self):
        
        while True:
            try:
                s.settimeout(None)
                reply,cIp=s.recvfrom(1024)
                self.textbox.config(state=NORMAL)
                self.textbox.insert(END,reply.decode()+'\n')
                self.textbox.config(state=DISABLED)
                
            except:
                break


    def validate_login(self):
        username = self.username.get()
        password = self.password.get()
        if username == '' or password == '':
              messagebox.showinfo('Error','Please enter all the fields')
        else:
            if validate_login(username,password):
                try:
                    s.sendto(f'login:{username}'.encode(),serverAddr)
                    s.settimeout(2)
                    self.login.pack_forget()
                    self.mainpage.pack(fill='both',expand=True)
                    get_message = threading.Thread(target=self.get_message)
                    get_message.start()
                    self.l1.config(text=username)
                    self.root.title(f'Chatroom:{username}')
                    self.textbox.config(state=NORMAL)
                    messages = getMessage()
                    values = set([x.strftime('%Y-%m-%d') for x in map(lambda x:x[2], messages)])
                    newlist = [[y for y in messages if y[2].strftime('%Y-%m-%d')==x] for x in values]

                    for i in newlist[::-1]:
                        date = i[0][2].strftime('%Y-%m-%d')
                        self.textbox.insert(END,f'{date}\n')
                        for j in i:
                            us = j[1]
                            if j[1] == username:
                                sql = f"[You]-[{j[2].strftime('%H:%M:%S')}]: {j[3]}"
                            else:
                                sql = f"[{j[1]}]-[{j[2].strftime('%H:%M:%S')}]: {j[3]}"
                            self.textbox.insert(END,sql+'\n')
                        self.textbox.insert(END,'\n')
                    self.textbox.config(state=DISABLED)
                    self.root.eval('tk::PlaceWindow . center')
                        
                except socket.timeout:
                    messagebox.showinfo('Error','Connection timed out\nServer Down')
                    self.root.destroy()
            else:
                messagebox.showinfo('Error','Invalid username or password')
                self.username.set('')
                self.password.set('')
    
            
   

client = APP()
