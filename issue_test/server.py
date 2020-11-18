#!/usr/bin/env python3
from pygroupsig import groupsig
from pygroupsig import signature
from pygroupsig import grpkey
from pygroupsig import mgrkey
from pygroupsig import gml
from pygroupsig import identity
from pygroupsig import constants
from pygroupsig import message

import json, socket
HOST = "127.0.0.1"
ISSUER_PORT = 11001
RCV_SIZE = 8192

class Server:
    
    def __init__(self):
        self.gpk = None
        self.myTokenTable = {}
        self.myGml = {}
        
        self.setup()
        # Need to update server's secret key
    
    
    # Load gpk
    def setup(self):
        request = {"gpk":"request"}
        request_json = json.dumps(request)
        
        # 방역당국에 gpk 요청
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, ISSUER_PORT))
        client_socket.send(request_json.encode())
        gpk_json = client_socket.recv(RCV_SIZE)
        self.gpk = json.loads(gpk_json)
        
        client_socket.close()
        return
    
    
    # Create valid token
    def createToken(self, id):
        # 시간 결합해서 임의의 토큰 어떻게든 발행
        pass
    
    
    # Create sign for token
    def createSign(self, data):
        # 서버 자체 개인키를 이용하면 됨
        pass
    
    
    # Login
    def requestToken(self, id, pw):
        # json 파일 파싱 필요
        
        # 데이터베이스에서 인증 과정
        
        # 인증 실패
        token = {"result":False}
        token_json = json.dumps(token, indent=4)
        
        # 인증 성공
        if id == "123" and pw == "123":
            # token = createToken(id)
            # sign = createSign(token)
            token = {"token":"this is temporary token{}".format(id)}
            token_json = json.dumps(token, indent=4)
            
            # 방역당국에게 토큰 전달
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, ISSUER_PORT))
            rtn = self.sendToken(token_json, client_socket)
            client_socket.close()

            # 자체 gml 추가
            if rtn:
                self.myTokenTable[token["token"]] = id
            
        return token_json # return 되면 client에게 response되기 때문에 다른 처리 하지 않음
    
    
    # Send token to target
    def sendToken(self, token, target):
        target.send(token.encode())
        
        response_json = target.recv(RCV_SIZE)
        response = json.loads(response_json)
        
        return response["result"]
    
    
    # Request Add Server's Gml 
    def requestAddGml(self, token, sign):
        # 실패 시 반환 값
        result_json = json.dumps({"result":False})
        
        if self.myTokenTable.get(token) == None:
            return result_json

        id = self.myTokenTable.get(token)
        
        # 방역당국에게 토큰 전달
        # 여기서는 수신한 json파일 그대로 넘겨주면 됨 
        # (내 코드에서는 분해됐다고 가정했기 때문에 새로 재조합)
        token_json = json.dumps({"token":token, "sign":sign})
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, ISSUER_PORT))
        gmlId = self.sendToken(token_json, client_socket)
        client_socket.close()
        
        # 요청 실패
        if gmlId < 0:
            return result_json
        
        # 방역당국의 gml idx와 내 서버의 사용자 id 맵핑
        self.myGml[gmlId] = id
        
        return json.dumps({"result":True})