#!/usr/bin/env python3
from pygroupsig import groupsig, signature, constants
from pygroupsig import grpkey, mgrkey, gml
from pygroupsig import identity, message
import time


class Issuer:
    
    TYPE_USER = 1
    TYPE_STORE = 2
    
    def __init__(self):
        SEED = 0
        groupsig.init(constants.BBS04_CODE, SEED)
        
        # 기존에 초기화 했던 적 있는 경우
        # with open(bbs04, "r") as f:
        #     base64GroupSig = f.readline().strip()
        
        bbs04_user = groupsig.setup(constants.BBS04_CODE)
        self.gpk_user = bbs04_user["grpkey"]
        self.gml_user = bbs04_user["gml"]
        self.msk_user = bbs04_user["mgrkey"]
        
        bbs04_store = groupsig.setup(constants.BBS04_CODE)
        self.gpk_store = bbs04_store["grpkey"]
        self.gml_store = bbs04_store["gml"]
        self.msk_store = bbs04_store["mgrkey"]
    
    
    # Send manager secret key
    def requestGpk(self, group_type):
        # 타입에 따라서 gpk 반환 필요
        if group_type == Issuer.TYPE_USER:
            base64_gpk = grpkey.grpkey_export(self.gpk_user)
            response = {"gpk":base64_gpk}
        if group_type == Issuer.TYPE_STORE:
            base64_gpk = grpkey.grpkey_export(self.gpk_store)
            response = {"gpk":base64_gpk}
        
        return response
    
    
    # Send manager secret key
    def requestMsk(self):
        pass
    
    
    # Receive a token
    def requestValidateToken(self, token):
        # 검증 실패 시 response (시간초과)
        response = {"result":False}
        
        # group_type = None
        group_type = Issuer.TYPE_USER
        
        # failed validatation
        # 타입에 따른 그룹의 키가 아닐 경우 return response
        # 시간 초과시 return response
        
        # 적법한 token
        response = self.addMember(group_type)
        
        return response
    
    
    # Add member -> return msg1
    def addMember(self, group_type):
        # group에 따른 멤버 추가
        if group_type == Issuer.TYPE_USER:
            msg1 = groupsig.join_mgr(0, self.msk_user, self.gpk_user, gml=self.gml_user)
            base64Msg1 = message.message_to_base64(msg1)
            
            response = {"msg1":base64Msg1}
            return response
        if group_type == Issuer.TYPE_STORE:
            msg1 = groupsig.join_mgr(0, self.msk_store, self.gpk_store, gml=self.gml_store)
            base64Msg1 = message.message_to_base64(msg1)
            
            response = {"msg1":base64Msg1}
            return response
    
    
    # Request to find the signatory
    def requestGmlId(self, token, sign):
        # 토큰에서 가입 type을 추출해야 함 (일반 사용자 or 점주)
        group_type = Issuer.TYPE_USER
        
        id = -1
        if group_type == Issuer.TYPE_USER:
            tokenSig = signature.signature_import(constants.BBS04_CODE, sign)
            try:
                member = groupsig.open(tokenSig, self.msk_user, self.gpk_user, self.gml_user)
                id = identity.identity_to_string(member)
            except Exception as e:
                print("He is not in the gml?")
                print(e)
        
        if group_type == Issuer.TYPE_STORE:
            tokenSig = signature.signature_import(constants.BBS04_CODE, sign)    
            try:
                member = groupsig.open(tokenSig, self.msk_store, self.gpk_store, self.gml_store)
                id = identity.identity_to_string(member)
            except Exception as e:
                print("He is not in the gml?")
                print(e)
        
        response = {"id":id}
        return response