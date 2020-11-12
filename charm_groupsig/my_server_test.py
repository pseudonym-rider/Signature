from manager import Manager
from charm.toolbox.pairinggroup import PairingGroup

def setting_manager(manager_obj):
    global gpk, gmsk
    gpk, gmsk = manager_obj.keygen_init()
    print('test gpk', gpk)
    print('test gmsk', gmsk)
    
    return (gpk, gmsk)
    

def add_member(manager_obj):
    gsk = manager_obj.keygen_mem()
    print('test gsk', gsk)


def verify_signature(manager_obj):
    sign = manager_obj.load_sign(int(input('member id')))
    return manager_obj.verify(gpk, input('message : '), sign)


def open_signature(manager_obj):
    sign = manager_obj.load_sign(int(input('member id')))
    return manager_obj.open(gpk, gmsk, input('message : '), sign)


if __name__=='__main__':
    group = PairingGroup('MNT224')

    manager_obj = Manager(group)
    
    gpk, gmsk = setting_manager(manager_obj)
    manager_obj.save_gpk()
    
    i = 0
    while True:
        print('--- menu ---')
        # print('1. key gen (init)')
        print('2. member add')
        print('3. verify signature')
        print('4. open signature')
        
        menu = int(input())
        if menu == 1:
            # setting_manager(manager_obj)
            pass
        elif menu == 2:
            add_member(manager_obj)
        elif menu == 3:
            print('verify result : ', verify_signature(manager_obj))
        elif menu == 4:
            print('open result : ', open_signature(manager_obj))
