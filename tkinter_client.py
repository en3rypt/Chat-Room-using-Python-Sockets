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



# # import all the required  modules
# import socket
# import threading
# from tkinter import *
# from tkinter import font
# from tkinter import ttk
 
# # import all functions /
# #  everything from chat.py file
# from chat import *
 
# PORT = 5050
# SERVER = "192.168.0.103"
# ADDRESS = (SERVER, PORT)
# FORMAT = "utf-8"
 
# # Create a new client socket
# # and connect to the server
# client = socket.socket(socket.AF_INET,
#                       socket.SOCK_STREAM)
# client.connect(ADDRESS)
 
 
# # GUI class for the chat
# class GUI:
#     # constructor method
#     def __init__(self):
       
#         # chat window which is currently hidden
#         self.Window = Tk()
#         self.Window.withdraw()
         
#         # login window
#         self.login = Toplevel()
#         # set the title
#         self.login.title("Login")
#         self.login.resizable(width = False,
#                              height = False)
#         self.login.configure(width = 400,
#                              height = 300)
#         # create a Label
#         self.pls = Label(self.login,
#                        text = "Please login to continue",
#                        justify = CENTER,
#                        font = "Helvetica 14 bold")
         
#         self.pls.place(relheight = 0.15,
#                        relx = 0.2,
#                        rely = 0.07)
#         # create a Label
#         self.labelName = Label(self.login,
#                                text = "Name: ",
#                                font = "Helvetica 12")
         
#         self.labelName.place(relheight = 0.2,
#                              relx = 0.1,
#                              rely = 0.2)
         
#         # create a entry box for
#         # tyoing the message
#         self.entryName = Entry(self.login,
#                              font = "Helvetica 14")
         
#         self.entryName.place(relwidth = 0.4,
#                              relheight = 0.12,
#                              relx = 0.35,
#                              rely = 0.2)
         
#         # set the focus of the cursor
#         self.entryName.focus()
         
#         # create a Continue Button
#         # along with action
#         self.go = Button(self.login,
#                          text = "CONTINUE",
#                          font = "Helvetica 14 bold",
#                          command = lambda: self.goAhead(self.entryName.get()))
         
#         self.go.place(relx = 0.4,
#                       rely = 0.55)
#         self.Window.mainloop()
 
#     def goAhead(self, name):
#         self.login.destroy()
#         self.layout(name)
         
#         # the thread to receive messages
#         rcv = threading.Thread(target=self.receive)
#         rcv.start()
 
#     # The main layout of the chat
#     def layout(self,name):
       
#         self.name = name
#         # to show chat window
#         self.Window.deiconify()
#         self.Window.title("CHATROOM")
#         self.Window.resizable(width = False,
#                               height = False)
#         self.Window.configure(width = 470,
#                               height = 550,
#                               bg = "#17202A")
#         self.labelHead = Label(self.Window,
#                              bg = "#17202A",
#                               fg = "#EAECEE",
#                               text = self.name ,
#                                font = "Helvetica 13 bold",
#                                pady = 5)
         
#         self.labelHead.place(relwidth = 1)
#         self.line = Label(self.Window,
#                           width = 450,
#                           bg = "#ABB2B9")
         
#         self.line.place(relwidth = 1,
#                         rely = 0.07,
#                         relheight = 0.012)
         
#         self.textCons = Text(self.Window,
#                              width = 20,
#                              height = 2,
#                              bg = "#17202A",
#                              fg = "#EAECEE",
#                              font = "Helvetica 14",
#                              padx = 5,
#                              pady = 5)
         
#         self.textCons.place(relheight = 0.745,
#                             relwidth = 1,
#                             rely = 0.08)
         
#         self.labelBottom = Label(self.Window,
#                                  bg = "#ABB2B9",
#                                  height = 80)
         
#         self.labelBottom.place(relwidth = 1,
#                                rely = 0.825)
         
#         self.entryMsg = Entry(self.labelBottom,
#                               bg = "#2C3E50",
#                               fg = "#EAECEE",
#                               font = "Helvetica 13")
         
#         # place the given widget
#         # into the gui window
#         self.entryMsg.place(relwidth = 0.74,
#                             relheight = 0.06,
#                             rely = 0.008,
#                             relx = 0.011)
         
#         self.entryMsg.focus()
         
#         # create a Send Button
#         self.buttonMsg = Button(self.labelBottom,
#                                 text = "Send",
#                                 font = "Helvetica 10 bold",
#                                 width = 20,
#                                 bg = "#ABB2B9",
#                                 command = lambda : self.sendButton(self.entryMsg.get()))
         
#         self.buttonMsg.place(relx = 0.77,
#                              rely = 0.008,
#                              relheight = 0.06,
#                              relwidth = 0.22)
         
#         self.textCons.config(cursor = "arrow")
         
#         # create a scroll bar
#         scrollbar = Scrollbar(self.textCons)
         
#         # place the scroll bar
#         # into the gui window
#         scrollbar.place(relheight = 1,
#                         relx = 0.974)
         
#         scrollbar.config(command = self.textCons.yview)
         
#         self.textCons.config(state = DISABLED)
 
#     # function to basically start the thread for sending messages
#     def sendButton(self, msg):
#         self.textCons.config(state = DISABLED)
#         self.msg=msg
#         self.entryMsg.delete(0, END)
#         snd= threading.Thread(target = self.sendMessage)
#         snd.start()
 
#     # function to receive messages
#     def receive(self):
#         while True:
#             try:
#                 message = client.recv(1024).decode(FORMAT)
                 
#                 # if the messages from the server is NAME send the client's name
#                 if message == 'NAME':
#                     client.send(self.name.encode(FORMAT))
#                 else:
#                     # insert messages to text box
#                     self.textCons.config(state = NORMAL)
#                     self.textCons.insert(END,
#                                          message+"\n\n")
                     
#                     self.textCons.config(state = DISABLED)
#                     self.textCons.see(END)
#             except:
#                 # an error will be printed on the command line or console if there's an error
#                 print("An error occured!")
#                 client.close()
#                 break
         
#     # function to send messages
#     def sendMessage(self):
#         self.textCons.config(state=DISABLED)
#         while True:
#             message = (f"{self.name}: {self.msg}")
#             client.send(message.encode(FORMAT))   
#             break   
 
# # create a GUI class object
# g = GUI()