from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
from nac.decryptionpolicy.run import DecryptionPolicy
from nac.encryptionpolicy.run import EncryptionPolicy
import sys, os
from ndn.encoding import *
from ndn.security import *
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from nac.utils.tlvmodels import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import ECC
from nac.utils.ECIES import *


logging.basicConfig(
    format='[{asctime}]{levelname}:{message}',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    style='{'
)

class Encryptor:
    def __init__(self, amPrefix):
        self.amPrefix = amPrefix
    
    def parseSchema(self, schema):
        ep = EncryptionPolicy(schema)
        return ep.execute()
        
    async def fetchKEK(self, app, KekNames):
        keks = {}
        for KekName in KekNames:
            print(f'Sending Interest {Name.to_str(KekName)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, kek = await app.express_interest(
                KekName, must_be_fresh=True, can_be_prefix=True, lifetime=6000
            )
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(kek) if kek else None)
            keks[Name.to_str(KekName)] = kek
        return keks
        
    def getKEKGrans(self, dic, name):
        try:
            for key, val in dic.items():
                key = Name.from_str(key)
                for i, n in enumerate(key):
                    if (Name.to_str([n]) == '/_' or n == name[i]):
                        if (i == len(key) - 1):
                            return val
                        continue
                    else:
                        break
        except:
            return None
    
    def getKEKName(self, keychain, dic, name):
        grans = self.getKEKGrans(dic, name)
        res = []
        for gran in grans:
            s = f"{self.amPrefix}/NAC{gran}/KEK"
            id = keychain.touch_identity(s)
            n = id.default_key().name
            print(n)
            res.append(n)
        return res
                
    def buildKeklistName(self, contentName):
        return f"{self.amPrefix}/NAC/KEKList{contentName}/_/_/CK"
    
    def buildckName(self, contentName, kek):
        return f"{contentName}/CK/ENCRYPTED-BY{kek}"
        
    def generate_ck(self):
        ck = get_random_bytes(32)
        return ck
    
    def encrypt_content(self, content):
        encryptedContent = EncryptedContent()
        encryptedContent.inner = NestedModel()
        ck = self.generate_ck()
        cipher_encrypt = AES.new(ck, AES.MODE_CFB)
        ciphered_bytes = cipher_encrypt.encrypt(content)
        iv = cipher_encrypt.iv
        ciphered_data = ciphered_bytes
        print(ciphered_data, iv, type(ciphered_data), content

