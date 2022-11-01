from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
import sys
from accessmanager import AccessManager

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

def publishKEKs(keks):
    for name in keks:
        content = 'key'  #actual key needs to be generated
        print(name)
        @app.route(name)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            app.put_data(name, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')

def main():
    encSchema = sys.argv[1]
    decSchema = sys.argv[2]
    amPrefix = '/Alice/Home'
    accessmanager = AccessManager(encSchema,decSchema,amPrefix)
    kekDic = accessmanager.buildKEKNames()
    publishKEKNames(kekDic)
            
    keks = accessmanager.buildKEKs(kekDic)
    publishKEKs(keks)
    print('Start serving ...')
    app.run_forever()

if __name__ == '__main__':
    main()


