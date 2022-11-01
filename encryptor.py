from typing import Optional
from ndn.app import NDNApp
#from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
from decryptionpolicy.run import DecryptionPolicy
from encryptionpolicy.run import EncryptionPolicy
import sys
from ndn.encoding import *
from tlvmodels import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


    
class Encryptor:
    def __init__(self,amPrefix):
        self.amPrefix = amPrefix
        
    def buildKeklistName(self,contentName):
        return self.amPrefix+'/NAC/KEKList'+contentName+'/_/_/CK'
        
    def generate_ck(self):
        ck = get_random_bytes(32)
        return ck
    
    def encrypt_content(self,content):
        encryptedContent = EncryptedContent()
        encryptedContent.inner = NestedModel()
        ck = self.generate_ck()
        print(ck)
        cipher_encrypt = AES.new(ck, AES.MODE_CFB)
        ciphered_bytes = cipher_encrypt.encrypt(content)
        iv = cipher_encrypt.iv
        ciphered_data = ciphered_bytes
        
        encryptedContent.inner.encryptedPayload = ciphered_data
        encryptedContent.inner.initializationVector = iv
        
        
        
        
        return encryptedContent.encode()
        


    def parseKEKNames(self,content):
        res = []
        model = KEKListModel.parse(bytes(content))
        for l in model.list:
            gran = bytes(l).decode()
            res.append(self.amPrefix+'/NAC'+gran+'/KEK')
        return res
