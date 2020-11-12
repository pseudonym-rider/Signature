#!/usr/bin/env python3
from pygroupsig import groupsig
from pygroupsig import signature
from pygroupsig import grpkey
from pygroupsig import mgrkey
from pygroupsig import gml
from pygroupsig import identity
from pygroupsig import constants
from pygroupsig import message

# Setup
def setup_manager():
    fname = input("input gpk file (if you don't have gpk file, press enter)").strip()
    bbs04 = None

    if fname == '':
        bbs04 = groupsig.setup(constants.BBS04_CODE) # BBS group signature
    else:
        groupsig.init(constants.BBS04_CODE, 0)
        with open(fname, "r") as f:
            b64gpk = f.readline()
            gpk = grpkey.grpkey_import(constants.BBS04_CODE, b64gpk)
            bbs04 = groupsig.setup(constants.BBS04_CODE, grpkey=gpk)
    
    gpk = bbs04['grpkey']   # group public key

    # share group public key
    with open("./gpk", "w") as f:
        b64gpk = grpkey.grpkey_export(gpk)
        f.write("{}".format(b64gpk))
    
    return bbs04


# Join
def join_setup():
    msg1 = groupsig.join_mgr(0, msk, gpk, gml = gml)    # Runs the manager side of join of the scheme.

    # share invite message
    with open("invitation", "w") as f:
        f.write("{}\n".format(message.message_to_base64(msg1)))
    
    print('send a invitation')
    return


# Verify
def verify(gpk):
    fname = input('write a signature file : ')

    with open(fname, "r") as f:
        msg = f.readline().rstrip()
        b64sig = f.readline().rstrip()

        sig = signature.signature_import(constants.BBS04_CODE, b64sig)
        result = groupsig.verify(sig, msg, gpk)

        if result == True:
            print ("{} ==> VALID signature.".format(fname))
        else:
            print ("{} ==> WRONG signature.".format(fname))
    
    return


# Open
def open_signature(msk, gpk, gml):
    fname = input('write a signature file : ')

    with open(fname, "r") as f:
        _ = f.readline()
        b64sig = f.readline().rstrip()

        sig = signature.signature_import(constants.BBS04_CODE, b64sig)
        id = groupsig.open(sig, msk, gpk, gml)

        mem = identity.identity_to_string(id)
        print("identity of the signature : {}".format(mem))
    
    return


if __name__ == "__main__":
    # something code...
    bbs = None
    gpk = None
    msk = None
    gml = None
    while True:
        print("---menu---")
        print("1. setup manager")
        print("2. join member")
        print("3. verify sign")
        print("4. open sign")
        print("5. quit")
        
        select = int(input().rstrip())
        
        if select == 1:
            bbs = setup_manager()
            gpk = bbs['grpkey']
            gml = bbs['gml']
            msk = bbs['mgrkey']
        elif select == 2:
            if bbs is None:
                print("setup first")
                continue
            join_setup()
        elif select == 3: 
            if bbs is None:
                print("setup first")
                continue
            verify(gpk)
        elif select == 4:  
            if bbs is None:
                print("setup first")
                continue
            open_signature(msk, gpk, gml)
        else: break
        
    groupsig.clear(constants.BBS04_CODE, bbs['config'])

