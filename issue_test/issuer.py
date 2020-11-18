#!/usr/bin/env python3
from pygroupsig import groupsig
from pygroupsig import signature
from pygroupsig import grpkey
from pygroupsig import mgrkey
from pygroupsig import gml
from pygroupsig import identity
from pygroupsig import constants
from pygroupsig import message
import json, time


class Issuer:
    
    def __init__(self):
        SEED = 0
        groupsig.init(constants.BBS04_CODE, SEED)
        
        # 기존에 초기화 했던 적 있는 경우
        # with open(bbs04, "r") as f:
        #     base64GroupSig = f.readline().strip()
        
        bbs04 = groupsig.setup(constants.BBS04_CODE)
        self.gpk = bbs04["grpkey"]
        self.gml = bbs04["gml"]
        self.msk = bbs04["mgrkey"]
        self.validateToken = {}
    
    
    # Send manager secret key
    def sendMsk(self):
        pass
    
    
    # Check a received signature of the token with Server's public key
    def checkSign(self, token, sign):
        # 검증 성공 : token을 해시한 값 == sign의 내용
        return True
        # 검증 실패 : token을 해시한 값 != sign의 내용
        # return False
    
    
    # Receive a token
    def requestValidateToken(self, token, sign):
        # 검증 실패 시 response (시간초과)
        response_json = json.dumps({"result":False})
        
        # 검증 과정
        check = self.checkSign(token, sign)
        
        # response 만들기
        if check:
            response_json = self.addMember()
        
        return response_json
    
    
    # Check two received tokens
    # def validate(self, sender, token):
    #     # 처음 받는 토큰
    #     if self.validateToken.get(token) == None:
    #         self.validateToken[token] = [sender]
    #         return False
        
    #     # 한명에게만 받은 토큰 (같은 송신자에 대한 중복 토큰)
    #     senderList = self.validateToken.get(token)
    #     if len(senderList) == 1 and sender in senderList:
    #         return False
        
    #     # user와 server에게 정확하게 받았음
    #     self.validateToken[token].append(sender)
        
    #     return True
    
    
    # Add member -> return usk
    def addMember(self):
        msg1 = groupsig.join_mgr(0, self.msk, self.gpk, gml=self.gml)
        base64Msg1 = message.message_to_base64(msg1)
        
        response_msg = {"msg1":base64Msg1}
        response_json = json.dumps(response_msg)
        
        return response_json
    
    
    # Request to find the signatory
    def requestGmlId(self, token, sign):
        tokenSig = signature.signature_import(constants.BBS04_CODE, sign)
        
        id = 0
        try:
            member = groupsig.open(tokenSig, self.msk, self.gpk, self.gml)
            id = identity.identity_to_string(member)
        except Exception as e:
            print("He is not in the gml?")
            print(e)
            id = -1
        
        result = {"id":id}
        result_json = json.dumps(result)
        
        return result_json