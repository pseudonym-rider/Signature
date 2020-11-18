import socket 
from _thread import *
import json
from issuer import Issuer

RCV_SIZE = 8192

def threaded(socket, addr, issuer): 
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
            if "sender" in key and "token" in key:
                # 토큰 업로드
                return_json = issuer.requestValidateToken(data["sender"], data["token"])
                
                # 토큰이 두개가 다 도착했는지 확인
                
                # 두 토큰이 정상이면 각각 값 전달
                # from == server : 


        except ConnectionResetError:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
        
    socket.close() 


HOST = "127.0.0.1"
ISSUER_PORT = 11001

issuer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
issuer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
issuer_socket.bind((HOST, ISSUER_PORT)) 
issuer_socket.listen() 

issuer = Issuer()

print('server start')

# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.
# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True: 
    print('wait')

    socket, addr = issuer_socket.accept() 
    start_new_thread(threaded, (socket, addr, issuer)) 

issuer_socket.close() 