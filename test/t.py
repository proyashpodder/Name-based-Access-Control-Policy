from Crypto.PublicKey import ECC

f = open('privKeys/97cc0c81777e988284f8030c4dfaef1f828daf64971ef1bcaa8a4ca3b1f50cbf.privkey', 'rb')
privKey = f.read()
eccKey = ECC.import_key(privKey)
