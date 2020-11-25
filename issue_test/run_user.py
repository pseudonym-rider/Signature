from user import User

u = User()
if not u.login():
    print("login fail")
    exit(0)

if not u.relayToken():
    print("relay fail")
    exit(0)

if not u.sendSign():
    print("fail to verify sign")
    exit(0)

print("success")