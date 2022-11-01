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




def main():
    #dp = DecryptionPolicy(sys.argv[1])
    #dic = dp.execute()
    encSchema = sys.argv[1]
    decSchema = sys.argv[2]
    amPrefix = '/Alice/Home'
    accessmanager = AccessManager(encSchema,decSchema,amPrefix)
    #encDic = accessmanager.parse_encryption_schema()
    #decDic = accessmanager.parse_decryption_schema()
    kekDic = accessmanager.buildKEKNames()
    #print(kekDic)
    

    app = NDNApp()
    '''#dic = {'home/user/alice/key':['/home','/home/bedroom'],
    #       'home/user/ruth/key':['home/guestroom'] }
    #formatPrint(dic)'''
    #dic = {'/edu/fiu/cs':['/student/proyash','/faculty/alex'],
    #       '/edu/ucla/cs': ['/xinyu']}
    # the consumer gets timeout. Maybe the issue can be wityh _ thing. check by removing that
    for key,val in kekDic.items():
        print(key,val)
        @app.route(key)
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            res = ''
            val = kekDic[n]
            '''for i in range(len(val)):
                print(dic[n][i])
                res += dic[n][i]+'#'''
            content = val
            #content = "Hello".encode()
            print(content)
            app.put_data(name, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')
            
    keks = accessmanager.buildKEKs(kekDic)
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
    print('Start serving ...')
    app.run_forever()

if __name__ == '__main__':
    main()


