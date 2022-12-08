import logging
import os,sys
from typing import Optional
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import *
from encryptor import Encryptor
from decryptor import Decryptor
from tlvmodels import *
from ndn.security import *
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

amPrefix = '/Alice/Home'
app = NDNApp()

        
async def main():
    try:
        basedir = os.path.dirname(os.path.abspath(sys.argv[0]))
        tpm_path = os.path.join(basedir, 'privKeys')
        pib_path = os.path.join(basedir, 'pib.db')
        keychain = KeychainSqlite3(pib_path, TpmFile(tpm_path))
        
        
        dec = Decryptor(amPrefix)
    
        contentName = '/Home/livingroom/camera/feed/1'
        identity = '/Home/user/Alice/KEY'
        id = keychain.touch_identity(identity)
        
        privKeyLoc = sha256(Name.to_bytes(id.default_key().name)).digest().hex() + '.privkey'
        f = open('privkeys/'+privKeyLoc, "rb")
        privKey = f.read()
        print(privKey)
        print(type(privKey))
        #print(type(privKey.encode()))
        
        name = Name.from_str(contentName)
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, encryptedContent = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            
        print(encryptedContent)
        encryptedModel = EncryptedContent.parse(encryptedContent)
        print(bytes(encryptedModel.inner.encryptedPayload),type(encryptedModel),bytes(encryptedModel.inner.initializationVector))
        encryptedPayload = bytes(encryptedModel.inner.encryptedPayload)
        iv = bytes(encryptedModel.inner.initializationVector)
        
        
        
        ckName = '/Home/livingroom/camera/feed/1/CK'
        modCKName = 'Home/livingroom/CK'
        name = Name.from_str(ckName)
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, ckData = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            
        print(bytes(ckData))
        kekNames = dec.parseCKNames(ckData)
        #print(kekNames)
        
        for kekName in kekNames:
            kdkName = kekName[:-4]+'/KDK/ENCRYPTED-BY'+ identity
            print(kdkName)
        
        ckNames = dec.buildCKName(ckName,kekNames)
        print(ckNames)
        
        '''name = Name.from_str('/Home/livingroom/CK/ENCRYPTED-BY/Alice/Home/NAC/Home/livingroom/KEK')
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=18000)}')
        data_name, meta_info, encryptedCK = await app.express_interest(
            name, must_be_fresh=False, can_be_prefix=False, lifetime=18000)
            
        if(encryptedCK):
            print('hola')
            print(bytes(encryptedCK))'''
        
        for key,value in ckNames.items():
            try:
                encryptedCK = ''
                name = Name.from_str(value)
                print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
                data_name, meta_info, encryptedCK = await app.express_interest(
                    name, must_be_fresh=False, can_be_prefix=False, lifetime=6000)
                    
                #if(encryptedCK):
                print(encryptedCK)
                #print(str(name), key)
                key = Name.normalize(key)
                print(key)
                kdkName = Name.to_str(key[:-3])+'/KDK/ENCRYPTED-BY'+ identity
                
                print(kdkName)
                
                try:
                    name = Name.from_str(kdkName)
                    print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
                    data_name, meta_info, kdk = await app.express_interest(
                    name, must_be_fresh=False, can_be_prefix=False, lifetime=6000)
                    
                    print(bytes(kdk))
                    #print(bytes(privKey))
                    #kdk = load_priv_key(bytes(kdk))
                    #print(kdk)
                    k = ECC.import_key(b64decode(privKey))
                    kdk = decrypt(k,bytes(kdk))
                    print(kdk)
                    
                    
                    ck = decrypt(ECC.import_key(b64decode(kdk)),bytes(encryptedCK))
                    print(ck)
                    
                    
                    aes_dec = AES.new(ck, AES.MODE_CFB, iv=iv)
                    msg = aes_dec.decrypt(encryptedPayload)
                    print("the message is: ")
                    print(msg, type(msg), str(msg))
                    txt = msg.decode('utf-8')
                    print(txt)
                
                except InterestNack as e:
                    print(f'Nacked with reason={e.reason}')
                except InterestTimeout:
                    print(f'Timeout')
                except InterestCanceled:
                    print(f'Canceled')
                except ValidationFailure:
                    print(f'Data failed to validate')
                    
                    
            except InterestNack as e:
                print(f'Nacked with reason={e.reason}')
            except InterestTimeout:
                print(f'Timeout')
            except InterestCanceled:
                print(f'Canceled')
            except ValidationFailure:
                print(f'Data failed to validate')
                
        
        
        
        
        
    except InterestNack as e:
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        print(f'Timeout')
    except InterestCanceled:
        print(f'Canceled')
    except ValidationFailure:
        print(f'Data failed to validate')
    #finally:
        #app.shutdown()


if __name__ == '__main__':
    app.run_forever(after_start=main())

