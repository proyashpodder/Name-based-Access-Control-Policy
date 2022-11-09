import rsa
def generate_keys():
    pubKey, privKey = rsa.newkeys(1024)
    print(pubKey,privKey)
    pubKey = pubKey.save_pkcs1('PEM')
    privKey = privKey.save_pkcs1('PEM')
    print(pubKey,privKey)
    return pubKey,privKey

def load_keys(pubKey,prevKey):
    pubKey = rsa.PublicKey.load_pkcs1(pubKey)
    privKey = rsa.PrivateKey.load_pkcs1(privKey)
    return pubKey,privKey

def load_pub_key(pubKey):
    pubKey = rsa.PublicKey.load_pkcs1(pubKey)
    return pubKey
    
def load_priv_key(privKey):
    privKey = rsa.PrivateKey.load_pkcs1(privKey)
    return privKey
    
def encrypt(msg,key):
    return rsa.encrypt(msg,key)

def decrypt(ciphertext,key):
    #try:
    return rsa.decrypt(ciphertext,key)
    #except:
    #return False
