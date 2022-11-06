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

def publishKEKNames(kekDic):
    for key,val in kekDic.items():
        print(key,val)
        @app.route(key)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            res = ''
            val = kekDic[n]
            content = val
            print(content)
            app.put_data(name, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')

def publishKEKs(name,content):
    @app.route(name)
    def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
        n = Name.to_str(name)
        print(f'>> I: {Name.to_str(name)}, {param}')
        app.put_data(name, content=content, freshness_period=10000)
        print(f'<< D: {Name.to_str(name)}')
        print(MetaInfo(freshness_period=10000))
        print(f'Content: (size: {len(content)})')
        print('')

def publishKEKandKDK(keks):
    for name in keks:
        pubKey, privKey = generate_keys()
        publishKEKs(name, pubKey)
        #publishKDKs(privKey)

def main():
    encSchema = sys.argv[1]
    decSchema = sys.argv[2]
    amPrefix = '/Alice/Home'
    accessmanager = AccessManager(encSchema,decSchema,amPrefix)
    kekDic = accessmanager.buildKEKNames()
    publishKEKNames(kekDic)
            
    keks = accessmanager.buildKEKs(kekDic)
    #publishKEKandKDK(keks)#needs to add a dictionary of KDKs too after parsing like kek
    accessmanager.publishKEKandKDK(app, keks)
    print('Start serving ...')
    app.run_forever()

if __name__ == '__main__':
    main()


