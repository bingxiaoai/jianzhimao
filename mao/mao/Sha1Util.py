from hashlib import sha1

def jia_mi(str):
    sh = sha1()
    sh.update(str.encode())
    return sh.hexdigest() # str -- 40