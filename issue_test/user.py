#!/usr/bin/env python3
from pygroupsig import groupsig, signature, constants
from pygroupsig import memkey, grpkey, message
import requests


class User:
    
    URL = "http://127.0.0.1"
    # URL = "http://35.188.48.200"
    SERVER_PORT = ":80"
    ISSUER_PORT = ":5000"
    TYPE_USER = 1
    TYPE_STORE = 2
    
    def __init__(self):
        self.id = None
        self.pw = None
        self.token = None
        self.usk = None
        self.gpk = None
        self.group_type = None
        
    
    # Load gpk
    def setup(self):
        url = User.URL + "/request/gpk" + User.ISSUER_PORT
        request = {"group-type":self.group_type}
        response = requests.post(url, request)
        response = response.json()
        base64_gpk = response["gpk"]
        self.gpk = grpkey.grpkey_import(constants.BBS04_CODE, base64_gpk)
        return
    
    
    # Login (contact)
    def login(self):
        self.id = input("id : ").strip()
        self.pw = input("pw : ").strip()
        
        url = User.URL + "/request/token" + User.SERVER_PORT
        request = {"id":self.id, "pw":self.pw}
        response = requests.post(url, request)
        response = response.json()
        
        # login fail
        if "result" in response.keys():
            print("fail to login")
            return False
        
        # login success and receive token
        self.token = response['token']
        
        # token에서 받은 그룹 유형에 따라서 gpk 요청
        self.group_type = User.TYPE_USER
        self.setup()
        
        return True
    
    
    # Relay token from server to issuer
    def relayToken(self):
        url = User.URL + "/request/valid-token" + User.ISSUER_PORT
        request = {"token":self.token}
        response = requests.post(url, request)
        response = response.json()
        
        # fail to validate token
        if "result" in response.keys():
            print("fail to validate token from issuer")
            return False
        
        base64_msg1 = response["msg1"]
        msg1 = message.message_from_base64(base64_msg1)
        msg2 = groupsig.join_mem(1, self.gpk, msgin = msg1)
        self.usk = msg2["memkey"]
        
        return True
    
    
    # Make message for sign
    def makeMessage(self):
        # 수정 필요
        target = self.id + "\n" + self.token
        return target
    
    
    # Make a signature of the message
    def makeSign(self, message):
        pass
    
    
    # Receive user secret key and group public key
    def sendSign(self):
        message = self.makeMessage()
        base64_sign = self.makeSign(message)
        
        url = User.URL + "/request/add-member" + User.SERVER_PORT
        request = {"uid":self.id, "token":self.token, "sign":sign}
        response = requests.post(url, request)
        response = response.json()
        
        if response["result"] == False:
            # 초기화 이렇게 시키면 되려나?
            self.id = None
            self.pw = None
            self.group_type = None
            self.gpk = None
            self.usk = None
            self.token = None
        
        return response["result"]
        