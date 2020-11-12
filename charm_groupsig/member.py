from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.PKSig import PKSig
import pickle
from collections import deque

import traceback

debug=True

class Member(PKSig):
    
    def __init__(self, groupObj, gamma=None, gpk=None, gmsk=None, gsk=None):
        PKSig.__init__(self)
        global group
        group = groupObj
        
        if gamma != None:
            self.gamma = gamma
        else:
            self.gamma = {}
        if gpk != None:
            self.gpk = gpk
        else:
            self.gpk = {}
        if gmsk != None:
            self.gmsk = gmsk
        else:
            self.gmsk = {}
        if gsk != None:
            self.gsk = gsk
        else:
            self.gsk = None
    
    
    def load_gpk(self):
        try:
            with open('group_public_key.pickle', 'rb') as f:
                save = pickle.load(f)
                for k, v in save:
                    self.gpk[k] = group.deserialize(v)
            print(self.gpk)
            return True
        
        except Exception as e:
            print('exception', e)
            return False


    def load_gsk(self, number = 0, isManager=False):
        try:
            with open('group_secret_key{}.pickle'.format(number), 'rb') as f:
                save = pickle.load(f)
                tmp = []
                for i in range(2):
                    tmp.append(group.deserialize(save[i]))
                self.gsk = tuple(tmp)
            return True
        
        except Exception as e:
            print('exception', e)
            return False

    
    def save_sign(self, number, sign):
        save = deque()
        for k, v in sign.items():
            save.append([k, group.serialize(v)])
        
        try:
            with open('sign_value{}.pickle'.format(number), 'wb') as f:
                pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            return True

        except Exception:
            return False
    
    
    def sign(self, M):
        alpha, beta = group.random(), group.random()
        A, x = self.gsk[0], self.gsk[1]

        T1 = self.gpk['u'] ** alpha
        T2 = self.gpk['v'] ** beta
        T3 = A * (self.gpk['h'] ** (alpha + beta))
        
        delta1 = x * alpha
        delta2 = x * beta
        r = [group.random() for i in range(5)]
        
        R1 = self.gpk['u'] ** r[0]
        R2 = self.gpk['v'] ** r[1]
        R3 = (pair(T3, self.gpk['g2']) ** r[2]) * (pair(self.gpk['h'], self.gpk['w']) ** (-r[0] - r[1])) * (pair(self.gpk['h'], self.gpk['g2']) ** (-r[3] - r[4]))
        R4 = (T1 ** r[2]) * (self.gpk['u'] ** -r[3])
        R5 = (T2 ** r[2]) * (self.gpk['v'] ** -r[4])
        
        c = group.hash((M, T1, T2, T3, R1, R2, R3, R4, R5), ZR)
        s1, s2 = r[0] + c * alpha, r[1] + c * beta
        s3, s4 = r[2] + c * x, r[3] + c * delta1
        s5 = r[4] + c * delta2
        return {'T1':T1, 'T2':T2, 'T3':T3, 'c':c, 's_alpha':s1, 's_beta':s2, 's_x':s3, 's_delta1':s4, 's_delta2':s5}
    