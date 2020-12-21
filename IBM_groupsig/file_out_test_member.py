#!/usr/bin/env python3
from pygroupsig import groupsig
from pygroupsig import signature
from pygroupsig import memkey
from pygroupsig import grpkey
from pygroupsig import constants
from pygroupsig import message
import os


# Setup
def setup_member():
    groupsig.init(constants.BBS04_CODE, 0)

    gpk = None
    gpkpath = os.path.join(os.getcwd(), 'gpk')

    with open(gpkpath, "r") as f:
        b64gpk = f.readline().strip()
        print(b64gpk)
        print(len(b64gpk))
        # 2868 b64
        # 2150 bytes

        gpk = grpkey.grpkey_import(constants.BBS04_CODE, b64gpk)

    return gpk


# Join
def join(gpk):
    join_message = None

    with open("invitation", "r") as f:
        invite_message = f.readline()
        msg1 = message.message_from_base64(invite_message)
        join_message = groupsig.join_mem(1, gpk, msgin = msg1)
    
    return join_message


# Sign
def sign(usk, gpk):
    fname = input('input file name')

    with open(fname, "w") as f:
        msg = input('input message')
        sign = groupsig.sign(msg, usk, gpk)
        b64sign = signature.signature_export(sign)

        f.write("{}\n{}\n".format(msg, b64sign))
    
    return


if __name__ == "__main__":
    # something code...
    gpk = None
    usk = None
    while True:
        print("---menu---")
        print("1. setup member")
        print("2. join member")
        print("3. sign message")
        print("5. quit")
        
        select = int(input().rstrip())
        
        if select == 1:
            gpk = setup_member()
        elif select == 2: 
            if gpk is None:
                print('setup first (get group public key)')
                continue
            join_msg = join(gpk)
            usk = join_msg['memkey']
            print(memkey.memkey_export(usk))
        elif select == 3: 
            if gpk is None:
                print('setup first (get group public key)')
                continue
            sign(usk, gpk)
        else: break
