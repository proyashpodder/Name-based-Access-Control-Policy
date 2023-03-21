from nac.encryptionpolicy.run import EncryptionPolicy
import sys

encSchema = sys.argv[1]

ep = EncryptionPolicy(encSchema)
res = ep.execute()

print(res)
