#!/usr/bin/env python3
from pygroupsig import grpkey, constants
from flask import request, jsonify
import requests


class Server:
    
    _ISSUER_URL = "http://172.17.0.3"
    # _ISSUER_URL = "http://127.0.0.1"
    _ISSUER_PORT = "5000"
    TYPE_USER = 1
    TYPE_STORE = 2
    
    def __init__(self):
        self.gpk_user = None
        self.my_user_token_table = {}
        self.my_user_gml = {}
        
        self.gpk_store = None
        self.my_store_token_table = {}
        self.my_store_gml = {}
        
        self.setup()
        # Need to update server's secret key
    
    
    # Load gpk
    def setup(self):
        # 방역당국에 user group gpk 받아옴
        url = Server._ISSUER_URL + "/request/gpk" + Server._ISSUER_PORT
        request = {"group-type":Server.TYPE_USER}
        response = requests.post(url, request)
        response = response.json()
        base64_gpk = response["gpk"]
        self.gpk_user = grpkey.grpkey_import(constants.BBS04_CODE, base64_gpk)
        
        # 방역당국에 store group gpk 받아옴
        url = Server._ISSUER_URL + "/request/gpk" + Server._ISSUER_PORT
        request = {"group-type":Server.TYPE_STORE}
        response = requests.post(url, request)
        response = response.json()
        base64_gpk = response["gpk"]
        self.gpk_store = grpkey.grpkey_import(constants.BBS04_CODE, base64_gpk)
        
        return
    
    
    # Create valid token
    def createToken(self, id):
        # 시간 결합해서 임의의 토큰 어떻게든 발행
        # token에 추가되야할 값은 id, 시간, 가입형태(개인, 점주 등)
        pass
    
    
    # Login
    def requestToken(self, id, pw):
        # 데이터베이스에서 인증 과정 ##########################################
        # 어디 소속으로 가입했는지 알아야 함 (어느 그룹인지)
        group_type = Server.TYPE_USER
        
        # 인증 실패
        token = {"result":False}
        
        # 인증 성공
        if id == "123" and pw == "123":
            # token = createToken(id, group_type)
            token = {"token":"this is temporary token-{}-{}".format(id, group_type)}
            
            # 토큰 관리
            if group_type == Server.TYPE_USER:
                self.my_user_token_table[id] = token["token"]
            if group_type == Server.TYPE_STORE:
                self.my_store_token_table[id] = token["token"]

        return token
    
    
    # Check token's creation time
    def validateToken(self, token):
        # 현재 시각과 Token 생성 시각 비교
        pass
    
    
    # Request Add Server's Gml 
    def requestAddGml(self, uid, token, sign):
        response = {"result":False}
        
        # token의 시간 비교 (validationToken(token)) 추가해야 함 ###########################
        if (uid not in self.my_user_token_table.keys() or 
            token != self.my_user_token_table[uid]):
            return response
        
        # 서버에 인증 요청
        url = Server._ISSUER_URL + "/request/gml-id" + Server._ISSUER_PORT
        request = {"token":token, "sign":sign}
        response = requests.post(url, request)
        response = response.json()
        gml_id = response["id"]
        
        if gml_id < 0:
            del(self.my_user_token_table[uid])
            return response
        
        # token에서 그룹타입 알아내야 함
        group_type = Server.TYPE_USER
        
        if group_type == Server.TYPE_USER:
            del(self.my_user_token_table[uid])
            self.my_user_gml[gml_id] = uid
            response["result"] = True
        if group_type == Server.TYPE_STORE:
            del(self.my_store_token_table[uid])
            self.my_store_gml[gml_id] = uid
            response["result"] = True
        
        return response