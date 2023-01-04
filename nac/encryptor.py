from typing import Optional
from ndn.app import NDNApp
#from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
from nac.decryptionpolicy.run import DecryptionPolicy
from nac.encryptionpolicy.run import EncryptionPolicy
import sys,os
from ndn.encoding import *
from ndn.security import *
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from nac.utils.tlvmodels import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import ECC
from nac.utils.ECIES import *

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

class Encryptor:
    def __init__(self,amPrefix):
        self.amPrefix = amPrefix
        
    
        
    def parseSchema(self,schema):
        ep = EncryptionPolicy(schema)
        return ep.execute()
        
    async def fetchKEK(self,app,KekNames):
        keks = {}
        for KekName in KekNames:
            print(f'Sending Interest {Name.to_str(KekName)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, kek = await app.express_interest(
                KekName, must_be_fresh=True, can_be_prefix=True, lifetime=6000)
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(kek) if kek else None)
            keks[Name.to_str(KekName)] = kek
        return keks
        
    def getKEKGrans(self,dic,name):
        try:
            for key,val in dic.items():
                key = Name.from_str(key)
                for i,n in enumerate(key):
                    if(Name.to_str([n])=='/_' or n == name[i]):
                        if(i==len(key)-1):
                            return val
                        continue
                    else:
                        break
        except:
            return None
    
    def getKEKName(self,keychain, dic,name):
        grans = self.getKEKGrans(dic,name)
        res = []
        for gran in grans:
            s = self.amPrefix+'/NAC'+gran+'/KEK'
            id = keychain.touch_identity(s)
            n = id.default_key().name
            print(n)
            res.append(n)
        return res
                
            
            
    def buildKeklistName(self,contentName):
        return self.amPrefix+'/NAC/KEKList'+contentName+'/_/_/CK'
    
    def buildckName(self,contentName,kek):
        return contentName+'/CK/ENCRYPTED-BY'+ kek
        
    def generate_ck(self):
        ck = get_random_bytes(32)
        return ck
    
    def encrypt_content(self,content):
        encryptedContent = EncryptedContent()
        encryptedContent.inner = NestedModel()
        ck = self.generate_ck()
        cipher_encrypt = AES.new(ck, AES.MODE_CFB)
        ciphered_bytes = cipher_encrypt.encrypt(content)
        iv = cipher_encrypt.iv
        ciphered_data = ciphered_bytes
        print(ciphered_data,iv, type(ciphered_data
        ),content)
        
        encryptedContent.inner.encryptedPayload = ciphered_data
        encryptedContent.inner.initializationVector = iv

        return ck, encryptedContent.encode()
        


    def parseKEKNames(self,content):
        res = []
        model = KEKListModel.parse(bytes(content))
        print(model, content)
        for l in model.list:
            gran = bytes(l).decode()
            res.append(self.amPrefix+'/NAC'+gran+'/KEK')
        return res
        
    def publishCKNames(self,app,contentName,keks):
        name = contentName+'/CK'
        res = []
        ckNamesModel = CKNamesModel()
        l = []
        for key,values in keks.items():
            l.append(key.encode())
        ckNamesModel.list = l
        res = ckNamesModel.encode()
        print(type(name), type(res))
        @app.route(name)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            app.put_data(n, content=res, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(res)})')
            print('')
        
        
    def publishCK(self,app,contentName, ck,keks):
        dic = {}
        for key,values in keks.items():
            print(key,values)
            ckName = self.buildckName(contentName,key)
            print (ckName, bytes(values))
            #pubKey = load_pub_key(bytes(values))
            #encryptedCK = encrypt(ck,pubKey)
            encryptedCK = encrypt(ECC.import_key(values),ck)
            print(ckName,encryptedCK)
            dic[ckName] = encryptedCK
            print(encryptedCK, ckName)
        #self.pc(app,dic)
            @app.route(ckName)
            def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
                n = Name.to_str(ckName)
                print(f'>> I: {Name.to_str(n)}, {param}')
                app.put_data(n, content= encryptedCK, freshness_period=10000)
                print(f'<< D: {Name.to_str(n)}')
                print(MetaInfo(freshness_period=10000))
                print(f'Content: (size: {len(encryptedCK)})')
                print('')
            
            
    def pc(self,app,dic):
        for key,val in dic.items():
            print(type(val))
            @app.route(key)
            def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
                n = Name.to_str(key)
                print(f'>> I: {Name.to_str(n)}, {param}')
                app.put_data(n, content= str(val), freshness_period=10000)
                print(f'<< D: {Name.to_str(n)}')
                print(MetaInfo(freshness_period=10000))
                print(f'Content: (size: {len(val)})')
                print('')
    
    def publishContent(self,app,contentName, content):
        print(contentName, content)
        @app.route(contentName)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(contentName)
            print(f'>> I: {Name.to_str(contentName)}, {param}')
            app.put_data(n, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(contentName)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')
            
            
    async def encode(self,app,keychain,schema,contentName,data_to_encrypt):
        try:
            dic = self.parseSchema(schema)
            KekNames = self.getKEKName(keychain, dic,Name.from_str(contentName))
            print(KekNames)
            
            
            keks = await self.fetchKEK(app,KekNames)
                
            ck, encryptedContent = self.encrypt_content(data_to_encrypt.encode())
            print(keks)
            self.publishCKNames(app,contentName,keks)
            #publish CK and Content
            self.publishCK(app,contentName,ck,keks)
            self.publishContent(app,contentName,encryptedContent)
        except:
            print('Something wrong')
