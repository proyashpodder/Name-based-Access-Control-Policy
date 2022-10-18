
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import logging
#from .run import DecryptionPolicy
#from decryptionpolicy.run import DecryptionPolicy
import decryptionpolicy
import sys
#import decryptionpolicy.lib

logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


def main():
    dp = DecryptionPolicy(sys.argv[1])
    dic = dp.execute()
    print(dic)
    app = NDNApp()
    #dic = {'home/user/alice/key':['/home','/home/bedroom'],
    #       'home/user/ruth/key':['home/guestroom'] }
    #dic = {'/edu/fiu/cs':['/student/proyash','/faculty/alex'],
    #       '/edu/ucla/cs': ['/xinyu']}

    for key,val in dic.items():
        @app.route(key)
        
        def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
            n = Name.to_str(name)
            print(f'>> I: {Name.to_str(name)}, {param}')
            res = ''
            val = dic[n]
            for i in range(len(val)):
                print(dic[n][i])
                res += dic[n][i]+'#'
            content = res.encode()
            print(content)
            app.put_data(name, content=content, freshness_period=10000)
            print(f'<< D: {Name.to_str(name)}')
            print(MetaInfo(freshness_period=10000))
            print(f'Content: (size: {len(content)})')
            print('')

    '''@app.route('/nac/kek')
    def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
        print(f'>> I: {Name.to_str(name)}, {param}')
        content = "Hola, world!".encode()
        app.put_data(name, content=content, freshness_period=10000)
        print(f'<< D: {Name.to_str(name)}')
        print(MetaInfo(freshness_period=10000))
        print(f'Content: (size: {len(content)})')
        print('')'''
    print('Start serving ...')
    app.run_forever()

if __name__ == '__main__':
    main()

