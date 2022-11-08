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
from encryption import *


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')






class Decryptor:
    def __init__(self,amPrefix):
        self.amPrefix = amPrefix
        
    def parseCKNames(self,content):
        res = []
        model = CKNamesModel.parse(bytes(content))
        for l in model.list:
            name = bytes(l).decode()
            res.append(name)
        return res
        
    def buildCKName(self,ckName,kekNames):
        res = []
        for kekName in kekNames:
            res.append(ckName+kekName)
        return res
    
