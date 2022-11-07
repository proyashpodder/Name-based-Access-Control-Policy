from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
import sys
from accessmanager import AccessManager
from encryption import *

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

app = NDNApp()



def main():
    encSchema = sys.argv[1]
    decSchema = sys.argv[2]
    amPrefix = '/Alice/Home'
    accessmanager = AccessManager(encSchema,decSchema,amPrefix)
    kekDic = accessmanager.buildKEKNames()
    kdkDic = accessmanager.buildKDKs()
    accessmanager.publishKEKNames(app,kekDic)
            
    keks = accessmanager.buildKEKs(kekDic)
    accessmanager.publishKEKandKDK(app, keks,kdkDic)
    print('Start serving ...')
    app.run_forever()

if __name__ == '__main__':
    main()


