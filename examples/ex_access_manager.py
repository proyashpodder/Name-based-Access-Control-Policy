from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
import sys,os
from ndn.security import TpmFile, KeychainSqlite3
from ndn.app_support.light_versec import compile_lvs, Checker, DEFAULT_USER_FNS
from nac.accessmanager import AccessManager
from nac.encryption import *

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


app = NDNApp()


def main():
    basedir = os.path.dirname(os.path.abspath(sys.argv[0]))
    tpm_path = os.path.join(basedir, 'privKeys')
    pib_path = os.path.join(basedir, 'pib.db')
    keychain = KeychainSqlite3(pib_path, TpmFile(tpm_path))
    
    #app = NDNApp(keychain=keychain)
    
    #b = keychain.touch_identity('/ndn/yakk')

        
    encSchema = sys.argv[1]
    decSchema = sys.argv[2]
    amPrefix = '/Alice/Home'
    accessmanager = AccessManager(encSchema,decSchema,amPrefix)
    accessmanager.run(app,keychain)
    #accessmanager.publishKEK(app,'/Alice/Home','hello'.encode())
    #kekDic = accessmanager.buildKEKNames()
    #print(kekDic)
    #kdkDic = accessmanager.buildKDKs()
    #print(kdkDic)
    #accessmanager.publishKEKNames(app,kekDic)
            
    #keks = accessmanager.buildKEKs(kekDic)
    #accessmanager.publishKEKandKDK(app, keks,kdkDic)
    print('Start serving ...')
    app.run_forever()

if __name__ == '__main__':
    main()


