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
        self.root.geometry("400x410")
        self.name = StringVar()
        self.msg = StringVar()
        self.login = Frame(self.root)
        self.login.pack(fill='both',expand=True)

        #crteate label
        self.name_label = Label(self.login,text="Enter your name: ")
        self.name_label.pack()
        #create entry
        self.name_entry = Entry(self.login,textvariable=self.name)
        self.name_entry.pack()
        #create button
        self.enter_button = Button(self.login,text="Enter",command=self.validate_login)
        self.enter_button.pack()



        
        #create mainpage frame
        self.mainpage = Frame(self.root)
        


        self.l1 = Label(self.mainpage,text='')
        self.l1.pack()
        #create textbox in root
        #create new frame
        self.frame = Frame(self.mainpage)
        self.frame.pack()
        #create textbox
        self.textbox = Text(self.frame,height=22,width=47)
        self.textbox.pack(side='left')
        #create scrollbar
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side='right',fill='y')
        #configure scrollbar
        self.scrollbar.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=self.scrollbar.set)
        self.textbox.config(state=DISABLED)

        #create new frame
        self.frame2 = Frame(self.mainpage)
        self.frame2.pack()
        #create input left side and button right side
        self.input_left = Entry(self.frame2,textvariable=self.msg,width=35,font=17)
        self.input_left.pack(side='left')
        self.button_right = Button(self.frame2,text='Send',font=17,command=self.send_message)
        self.button_right.pack(side='right')


        self.root.mainloop()

    def send_message(self):
        s.sendto(self.msg.get().encode(),serverAddr)
        self.input_left.delete(0,END)
        print('message sent')
            
    def get_message(self):
        
        while True:
            print('get message')
            try:
                s.settimeout(None)
                reply,cIp=s.recvfrom(1024)
                print(reply.decode())
                self.textbox.config(state=NORMAL)
                self.textbox.insert(END,reply.decode()+'\n')
                self.textbox.config(state=DISABLED)
                
            except:
                print('error')
                break


    def validate_login(self):
        name = self.name_entry.get()
        try:
            if name:
                s.sendto(name.encode(),serverAddr)
                s.settimeout(2)
                reply,cIp=s.recvfrom(1024)
                if reply:
                    print('messsaage sent')
                    print(reply.decode())
                    self.login.pack_forget()
                    self.mainpage.pack(fill='both',expand=True)
                    get_message = threading.Thread(target=self.get_message)
                    get_message.start()
                    self.l1.config(text=self.name.get())
                    print('thread started')
                else:
                    messagebox.showinfo('Error','Login Failed!\nTry again') 
            else:
                messagebox.showinfo('Error','Enter your name to continue') 
            
        except socket.timeout:
            print('timeout')
            messagebox.showinfo('Error','Connection timed out\nServer Down')
            self.root.destroy()
            
   

app = GUI()
