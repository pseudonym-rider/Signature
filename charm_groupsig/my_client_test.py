from member import Member
from charm.toolbox.pairinggroup import PairingGroup


if __name__=='__main__':
    group = PairingGroup('MNT224')
    member_obj = Member(group)
    
    print(member_obj.load_gpk())
    mem = int(input('member count : '))
    member_obj.load_gsk(mem)
    
    msg = input('message : ')
    signature = member_obj.sign(msg)
    
    member_obj.save_sign(mem, signature)