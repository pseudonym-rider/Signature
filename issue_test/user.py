#!/usr/bin/env python3
from pygroupsig import groupsig
from pygroupsig import signature
from pygroupsig import memkey
from pygroupsig import grpkey
from pygroupsig import constants
from pygroupsig import message

import socket
import json

HOST = "127.0.0.1"
SERVER_PORT = 10001
ISSUER_PORT = 11001
RCV_SIZE = 8192

class User:
    
    def __init__(self):
        self.id = None
        self.pw = None
        self.token = None
        self.usk = None
        self.gpk = None
        
        self.setup()
    
    
    # Load gpk
    def setup(self):
        request = {"gpk":"request"}
        request_json = json.dumps(request)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, ISSUER_PORT))
        
        client_socket.send(request_json.encode())
        
        gpk_json = client_socket.recv(RCV_SIZE)
        self.gpk = json.loads(gpk_json)
        
        client_socket.close()
        return
    
    
    # Login (contact)
    def login(self):
        self.id = input("id : ").strip()
        self.pw = input("pw : ").strip()
        
        # id : string
        # pw : string
        account_dict = {"id": self.id, "pw":self.pw}
        account_json = json.dumps(account_dict, indent=4)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        
        client_socket.send(account_json.encode())
        
        token_json = client_socket.recv(RCV_SIZE)
        print(token_json)
        self.token = json.loads(token_json)
        
        client_socket.close()
        
        return self.token
    
    
    # Relay token from server to issuer
    def relayToken(self):
        # send token to issuer
        token_json = json.dumps(self.token, indent=4)
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, ISSUER_PORT))
        client_socket.send(token_json.encode())
        
        # receive response
        result_json = client_socket.recv(RCV_SIZE)
        client_socket.close()
        
        print(result_json)
        result = json.loads(result_json)
        
        # receive msg1
        if "result" in result.keys():
            print("validation failed")
            return False
        
        # set user's secret key
        base64Msg1 = result["msg1"]
        
        msg1 = message.message_from_base64(base64Msg1)
        msg2 = groupsig.join_mem(1, self.gpk, msgin = msg1)
        self.usk = msg2["memkey"]
        
        return True
    
    
    # Make message for sign
    def makeMessage(self):
        # 수정 필요
        target = self.id + self.token
        return target
    
    
    # Receive user secret key and group public key
    def sendSign(self):
        # make message for sign
        message = self.makeMessage()
        
        # sign the message
        sign = groupsig.sign(message, self.usk, self.gpk)
        base64Sign = signature.signature_export(sign)
        
        sign_json = json.dumps({"uid":self.id, "token":self.token, "sign":base64Sign})
        
        # send
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, SERVER_PORT))
        client_socket.send(sign_json.encode())
        
        # receive response
        result_json = client_socket.recv(RCV_SIZE)
        client_socket.close()
        
        result = json.loads(result_json)
        if result["result"]:
            return True
        
        self.gpk = None
        self.usk = None
        self.token = None
        return False