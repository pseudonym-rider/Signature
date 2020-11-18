import socket 
from _thread import *
import json
from server import Server

RCV_SIZE = 8192

def threaded(socket, addr, server): 
    print('Connected by :', addr[0], ':', addr[1]) 
    
    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 

        try:
            data_json = socket.recv(RCV_SIZE)
            
            if not data_json: 
                print('Disconnected by ' + addr[0],':',addr[1])
                break

            data = dict()
            data = json.loads(data_json)
            key = data.keys()
            
            # login()
            if "id" in key and "pw" in key:
                return_json = server.requestToken(data["id"], data["pw"])
                
                # 사용자에게 토큰 전달
                socket.send(return_json.encode())
                


        except ConnectionResetError:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
        
    socket.close() 


HOST = "127.0.0.1"
SERVER_PORT = 10001
ISSUER_PORT = 11001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, SERVER_PORT)) 
server_socket.listen() 

server = Server()

print('server start')

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True: 
    print('wait')

    socket, addr = server_socket.accept() 
    start_new_thread(threaded, (socket, addr, server)) 

server_socket.close() 