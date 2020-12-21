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
    bbs04 = None

    print("1번 : 새로 시작")
    print("2번 : 불러오기")
    menu = int(input())
    
    if menu == 1:
        bbs04 = groupsig.setup(constants.BBS04_CODE) # BBS group signature
        gpk = bbs04['grpkey']
        msk = bbs04['mgrkey']
        GML = bbs04['gml']
        b64gpk = grpkey.grpkey_export(gpk)
        with open("./gpk", "w") as f:
            f.write(b64gpk)
        b64msk = mgrkey.mgrkey_export(msk)
        with open("./msk", "w") as f:
            f.write(b64msk)
        gml.gml_export(GML, bytes("./gml".encode()))
        
    elif menu == 2: 
        groupsig.init(constants.BBS04_CODE, 0)
        b64gpk = b64msk = None
        with open("./gpk", "r") as f:
            b64gpk = f.readline()
        with open("./msk", "r") as f:
            b64msk = f.readline()
        gpk = grpkey.grpkey_import(constants.BBS04_CODE, b64gpk)
        msk = mgrkey.mgrkey_import(constants.BBS04_CODE, b64msk)
        GML = gml.gml_import(constants.BBS04_CODE, bytes("./gml".encode()))
        bbs04 = {}
        bbs04["grpkey"] = gpk
        bbs04["mgrkey"] = msk
        bbs04["gml"] = GML
    
    return bbs04


# Join
def join_setup():
    msg1 = groupsig.join_mgr(0, msk, gpk, gml = group_member_list)    # Runs the manager side of join of the scheme.

    # share invite message
    with open("invitation", "w") as f:
        f.write("{}\n".format(message.message_to_base64(msg1)))
    
    # f = open("gml", "w")
    print("get_joinseq {}".format(groupsig.get_joinseq(constants.BBS04_JOIN_SEQ)))
    print("get_joinseq {}".format(groupsig.get_joinseq(constants.BBS04_CODE)))
    gml.gml_export(group_member_list, bytes("./gml".encode()))
    
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
    group_member_list = None
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
            group_member_list = bbs['gml']
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
            open_signature(msk, gpk, group_member_list)
        else: break
        
    groupsig.clear(constants.BBS04_CODE, bbs['config'])

