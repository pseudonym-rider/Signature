def save_gps(gps, time):
    with open("./gps-db", "a") as f:
        f.write(gps + "\n" + time + "\n")
    return True

def get_gps():
    response = None
    with open("./gps-db", "r") as f:
        response = f.readlines()
    return {"gps-db":response}