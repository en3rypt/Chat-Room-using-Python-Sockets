import socket
import threading
serverAddr=((socket.gethostname(),9999))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Server socket created")
BUFFER_SIZE = 1024

s.bind(serverAddr)

ips = {}


def handle_client():   
    while True:
        
        msg,cIp=s.recvfrom(1024)
        if cIp not in ips:
            ips[cIp] = msg.decode()
            print("Client connected: ",cIp)
            s.sendto(bytes("Welcome to the server",'utf-8'),cIp)
            continue
        else:
            s.sendto(bytes("Welcome back",'utf-8'),cIp)
            print("Message from client: ",msg.decode('utf-8'))
        # #send msg to all clients in ips
        # for ip in ips:
        #     if ip != cIp:
        #         s.sendto(msg,ip)

        

        
def start():
    while(True):
        
        thread = threading.Thread(target = handle_client())
        thread.start()
        
start()
