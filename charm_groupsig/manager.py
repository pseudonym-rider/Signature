from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.PKSig import PKSig
import pickle
from collections import deque

debug=True

class Manager(PKSig):
    
    def __init__(self, groupObj, gamma=None, gpk=None, gmsk=None, gsk=None):
        PKSig.__init__(self)
        global group
        group = groupObj
        
        self.gamma = gamma
        self.gpk = gpk
        self.gmsk = gmsk
        self.gsk_dict = gsk
        
    
    def keygen_init(self):
        g1, g2 = group.random(G1), group.random(G2)
        h = group.random(G1)
        xi1, xi2 = group.random(), group.random()

        u,v = h ** ~xi1, h ** ~xi2
        if self.gamma == None:
            self.gamma = group.random(ZR) 
        w = g2 ** self.gamma
        gpk = { 'g1':g1, 'g2':g2, 'h':h, 'u':u, 'v':v, 'w':w }
        gmsk = { 'xi1':xi1, 'xi2':xi2 }

        if self.gpk == None:
            self.gpk = gpk
        if self.gmsk == None:
            self.gmsk = gmsk
        if self.gsk_dict == None:
            self.gsk_dict = {}
        
        return (gpk, gmsk)
    
    
    def keygen_mem(self, n=1):
        x = [group.random(ZR) for i in range(n)]
        A = [self.gpk['g1'] ** ~(self.gamma + x[i]) for i in range(n)]

        if debug: print("\nSecret keys...")
        for i in range(n):
            size = len(self.gsk_dict.keys())
            if debug: 
                print("User %d: A = %s, x = %s" % (i, A[i], x[i]))
                print("The number of group member : %d" % (len(self.gsk_dict.keys())))
                # print("The number of group member : {}".format(self.gsk_dict))
            mem_key = (A[i], x[i])
            self.gsk_dict[i+size] = mem_key
            # self.gsk_dict[i+size] = A[i]
        
        self.save_gsk(i+size)
        
        return mem_key

    
    def verify(self, gpk, M, sigma):
        validSignature = False
        
        c, t1, t2, t3 = sigma['c'], sigma['T1'], sigma['T2'], sigma['T3']
        s_alpha, s_beta = sigma['s_alpha'], sigma['s_beta']
        s_x, s_delta1, s_delta2 = sigma['s_x'], sigma['s_delta1'], sigma['s_delta2']
        
        R1_ = (gpk['u'] ** s_alpha) * (t1 ** -c)
        R2_ = (gpk['v'] ** s_beta) * (t2 ** -c)
        R3_ = (pair(t3, gpk['g2']) ** s_x) * (pair(gpk['h'],gpk['w']) ** (-s_alpha - s_beta)) * (pair(gpk['h'], gpk['g2']) ** (-s_delta1 - s_delta2)) * ((pair(t3, gpk['w']) / pair(gpk['g1'], gpk['g2'])) ** c)
        R4_ = (t1 ** s_x) * (gpk['u'] ** -s_delta1)
        R5_ = (t2 ** s_x) * (gpk['v'] ** -s_delta2)
        
        c_prime = group.hash((M, t1, t2, t3, R1_, R2_, R3_, R4_, R5_), ZR)
        
        if c == c_prime:
            if debug: print("c => '%s'" % c)
            if debug: print("Valid Group Signature for message: '%s'" % M)
            validSignature = True
        else:
            if debug: print("Not a valid signature for message!!!")
        return validSignature
    
    
    def open(self, gpk, gmsk, M, sigma):
        t1, t2, t3, xi1, xi2 = sigma['T1'], sigma['T2'], sigma['T3'], gmsk['xi1'], gmsk['xi2']
        
        A_prime = t3 / ((t1 ** xi1) * (t2 ** xi2))
        return A_prime
    
    
    def save_gpk(self):
        save = deque()
        for k, v in self.gpk.items():
            save.append([k, group.serialize(v)])
        
        try:
            with open('group_public_key.pickle', 'wb') as f:
                pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            return True

        except Exception as e:
            print(e)
            return False

    
    def save_gsk(self, number=0, isManager=False):
        save = deque()
        for i in range(2):
            save.append(group.serialize(self.gsk_dict[number][i]))
        
        try:
            with open('group_secret_key{}.pickle'.format(number), 'wb') as f:
                pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            return True

        except Exception:
            return False

    
    def load_sign(self, number):
        try:
            signature = {}
            with open('sign_value{}.pickle'.format(number), 'rb') as f:
                save = pickle.load(f)
                for k, v in save:
                    signature[k] = group.deserialize(v)
            return signature

        except Exception:
            return False