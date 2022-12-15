from typing import Optional
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
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
from ECIES import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import ECC
from base64 import b64decode, b64encode


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
        res = {}
        for kekName in kekNames:
            res[kekName] = ckName+'/ENCRYPTED-BY'+kekName
        return res
        
        
    def getPrivkey(self,id):
        privKeyLoc = sha256(Name.to_bytes(id.default_key().name)).digest().hex() + '.privkey'
        f = open('privkeys/'+privKeyLoc, "rb")
        privKey = f.read()
        return privKey
        
    async def decode(self,app,keychain,contentName,identity):
        id = keychain.touch_identity(identity)
        privKey = self.getPrivkey(id)

        encryptedPayload, iv = await self.fetchContent(app,contentName)
        
        
        ckName = '/Home/livingroom/camera/feed/1/CK' #need to figure out how to get the CK name (either included in the encrypted payload or same prefix
        ckData = await self.fetchCKData(app,ckName)
        kekNames = self.parseCKNames(ckData)
        ckNames = self.buildCKName(ckName,kekNames)
        
        
        for key,value in ckNames.items():
            try:
                encryptedCK = await self.fetchEncryptedCK(app,value)
                    
                key = Name.normalize(key)
                
                kdkName = Name.to_str(key[:-3])+'/KDK/ENCRYPTED-BY'+ identity
                
                
                encryptedKDK = await self.fetchKDK(app,kdkName)
                    
                print(bytes(encryptedKDK))
                
                kdk = self.decryptKDK(encryptedKDK,privKey)

                
                ck = self.decryptCK(encryptedCK,kdk)
                
                txt = self.decodeContent(encryptedPayload,ck,iv)

            except:
                print('Something wrong')
        
        
        
        
        
    async def fetchContent(self,app,contentName):
        try:
            name = Name.from_str(contentName)
            print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, encryptedContent = await app.express_interest(
                name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
                
            print(encryptedContent)
            encryptedModel = EncryptedContent.parse(encryptedContent)
            #print(bytes(encryptedModel.inner.encryptedPayload),type(encryptedModel),bytes(encryptedModel.inner.initializationVector))
            encryptedPayload = bytes(encryptedModel.inner.encryptedPayload)
            iv = bytes(encryptedModel.inner.initializationVector)\
            
            return encryptedPayload,iv
        
        
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
        
        
    async def fetchCKData(self,app,ckName):
        try:
            name = Name.from_str(ckName)
            print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, ckData = await app.express_interest(
                name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            
            return ckData
                
                
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
    
    async def fetchKDK(self,app,kdkName):
        try:
            name = Name.from_str(kdkName)
            print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, kdk = await app.express_interest(
            name, must_be_fresh=False, can_be_prefix=False, lifetime=6000)
            
            return kdk
    
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
            
    async def fetchEncryptedCK(self,app,value):
        try:
            encryptedCK = ''
            name = Name.from_str(value)
            print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, encryptedCK = await app.express_interest(
                name, must_be_fresh=False, can_be_prefix=False, lifetime=6000)
                
            #if(encryptedCK):
            print(encryptedCK)
            return encryptedCK
            
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')
            
    def decryptKDK(self,encryptedKDK,privKey):
        k = ECC.import_key(b64decode(privKey))
        kdk = decrypt(k,bytes(encryptedKDK))
        print(kdk)
        return kdk
        
    def decryptCK(self,encryptedCK,kdk):
        ck = decrypt(ECC.import_key(b64decode(kdk)),bytes(encryptedCK))
        print(ck)
        return ck
        
    def decodeContent(self,encryptedPayload,ck,iv):
        aes_dec = AES.new(ck, AES.MODE_CFB, iv=iv)
        msg = aes_dec.decrypt(encryptedPayload)
        print("the message is: ")
        print(msg, type(msg), str(msg))
        txt = msg.decode()
        print(txt)
        return txt
    
                    
                    
            
        
    
