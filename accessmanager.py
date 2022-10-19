
from typing import Optional
from ndn.app import NDNApp
#from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
from decryptionpolicy.run import DecryptionPolicy
from encryptionpolicy.run import EncryptionPolicy
import sys
from ndn.encoding import *

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


class KEKListModel(TlvModel):
    list = RepeatedField(BytesField(0x83))

class AccessManager():
    def __init__(self,encSchema,decSchema,amPrefix):
        self.encSchema = encSchema
        self.decSchema = decSchema
        self.amPrefix = amPrefix
        
    
    

    def parse_encryption_schema(self):
        ep = EncryptionPolicy(self.encSchema)
        return ep.execute()
    
    def parse_decryption_schema(self):
        dp = DecryptionPolicy(self.decSchema)
        return dp.execute()
        
    def buildKEKNames(self):
        kekDic = {}
        dic = self.parse_encryption_schema()
        for key,values in dic.items():
            k = self.amPrefix + '/NAC/KEKList'+key+'/CK'
            
            kekListModel = KEKListModel()
            l = []
            for i,n in enumerate(values):
                l.append(n.encode())
            kekListModel.list = l
            res = kekListModel.encode()
            kekDic[k] = res
        return kekDic
            
                
            
        
    
    

