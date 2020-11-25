#!/usr/bin/env python3
from pygroupsig import groupsig, signature, constants
from pygroupsig import memkey, grpkey, message
import requests, json


class User:
    
    # URL = "http://127.0.0.1"
    URL = "http://35.188.48.200"
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
        groupsig.init(constants.BBS04_CODE, 0)
    
    # Load gpk
    def setup(self):
        headers = {"content-type":"application/json"}
        url = User.URL + User.ISSUER_PORT + "/request/gpk"
        request = {"group-type":self.group_type}
        response = requests.post(url, data=json.dumps(request), headers=headers)
        response = response.json()
        base64_gpk = response["gpk"]
        self.gpk = grpkey.grpkey_import(constants.BBS04_CODE, base64_gpk)
        return
    
    
    # Login (contact)
    def login(self):
        self.id = input("id : ").strip()
        self.pw = input("pw : ").strip()
        
        headers = {"content-type":"application/json"}
        url = User.URL + User.SERVER_PORT + "/request/token"
        request = {"id":self.id, "pw":self.pw}
        response = requests.post(url, data=json.dumps(request), headers=headers)
        response = response.json()
        
        # login fail
        if "result" in response.keys():
            print("fail to login")
            return False
        
        # login success and receive token
        self.token = response['token']
        
        # request gpk of each group type in token ################################
        self.group_type = User.TYPE_USER
        self.setup()
        
        return True
    
    
    # Relay token from server to issuer
    def relayToken(self):
        headers = {"content-type":"application/json"}
        url = User.URL + User.ISSUER_PORT + "/request/valid-token"
        request = {"token":self.token}
        response = requests.post(url, data=json.dumps(request), headers=headers)
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
    
    """
    # Make message for sign
    def makeMessage(self):
        # Need to fix.. ##############################################
        target = self.id + "\n" + self.token
        return target
    """
    
    # Make a signature of the message
    def makeSign(self, message):
        sign = groupsig.sign(message, self.usk, self.gpk)
        base64_sign = signature.signature_export(sign)
        return base64_sign
    
    
    # Receive user secret key and group public key
    def sendSign(self):
        # message = self.makeMessage()
        # base64_sign = self.makeSign(message)
        base64_sign = self.makeSign(self.token)
        
        headers = {"content-type":"application/json"}
        url = User.URL + User.SERVER_PORT + "/request/add-member"
        request = {"uid":self.id, "token":self.token, "sign":base64_sign}
        response = requests.post(url, data=json.dumps(request), headers=headers)
        response = response.json()
        
        if response["result"] == False:
            # initialize..?
            self.id = None
            self.pw = None
            self.group_type = None
            self.gpk = None
            self.usk = None
            self.token = None
        
        return response["result"]
        