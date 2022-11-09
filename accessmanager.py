
from typing import Optional
from ndn.app import NDNApp
from collections import defaultdict
#from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
from decryptionpolicy.run import DecryptionPolicy
from encryptionpolicy.run import EncryptionPolicy
import sys
from ndn.encoding import *
from tlvmodels import *
from encryption import *

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

#app = NDNApp()

class KEKListModel(TlvModel):
    list = RepeatedField(BytesField(0x83))
    
class KDKListModel(TlvModel):
    list = RepeatedField(BytesField(0x84))

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
        
    def buildKDKs(self):
        kdkDic = defaultdict(list)
        dic = self.parse_decryption_schema()
        for key,values in dic.items():
            for val in values:
                newKey = self.amPrefix+'/NAC'+val+'/KEK'
                kdkDic[newKey].append(key)
        return kdkDic
    
    def buildKDKnames(self,name,keys):
        print(name,keys)
        res = []
        for key in keys:
            res.append(name[:-4]+'/KDK/ENCRYPTED-BY'+key)
        return res
    
    def buildKEKs(self,dic):
        res = []
        for key,val in dic.items():
            model = KEKListModel.parse(bytes(val))
            for l in model.list:
                gran = bytes(l).decode()
                res.append (self.amPrefix+'/NAC'+gran+'/KEK')
        return res
    
    def publishKEK(self,app,name,content):
        @app.route(name)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            app.put_data(name, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')
            
    def publishKDK(self,app,name,content):
        print(name,content)
        @app.route(name)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            app.put_data(name, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')
            
    def publishKEKandKDK(self,app,keks,kdks):
        for name in keks:
            pubKey, privKey = generate_keys()
            self.publishKEK(app, name, pubKey)
            #publishKDKs(privKey)
            print(name, kdks)
            if(kdks[name]):
                kdkList = self.buildKDKnames(name,kdks[name])
                print (kdkList)
                for kdkName in kdkList:
                    self.publishKDK(app,kdkName,privKey) # need to encrypt by the key(e.g., alice's key, bob's key etc.
                    
    def publishKEKNames(self,app,kekDic):
        for key,val in kekDic.items():
            @app.route(key)
            def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
                n = Name.to_str(name)
                print(f'>> I: {Name.to_str(name)}, {param}')
                res = ''
                val = kekDic[n]
                content = val
                #print(content)
                app.put_data(name, content=content, freshness_period=10000)
                print(f'<< D: {Name.to_str(name)}')
                print(MetaInfo(freshness_period=10000))
                print(f'Content: (size: {len(content)})')
                print('')
            
                
            
        
    
    

