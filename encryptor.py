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






class Encryptor:
    def __init__(self,amPrefix):
        self.amPrefix = amPrefix
        
    def parseSchema(self,schema):
        ep = EncryptionPolicy(schema)
        return ep.execute()
        
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
    
    def getKEKName(self,dic,name):
        grans = self.getKEKGrans(dic,name)
        res = []
        for gran in grans:
            res.append(self.amPrefix+'/NAC'+gran+'/KEK')
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
            pubKey = load_pub_key(bytes(values))
            encryptedCK = encrypt(ck,pubKey)
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
