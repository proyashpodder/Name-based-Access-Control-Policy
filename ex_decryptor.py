import logging
from typing import Optional
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import *
from encryptor import Encryptor
from decryptor import Decryptor
from tlvmodels import KEKListModel


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

amPrefix = '/Alice/Home'
app = NDNApp()

        
async def main():
    try:
        dec = Decryptor(amPrefix)
    
        contentName = '/Home/livingroom'
        name = Name.from_str(contentName)
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, encryptedContent = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            
        print(encryptedContent)
        
        ckName = '/Home/livingroom/_/_/CK'
        name = Name.from_str(ckName)
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, ckData = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            
        kekNames = dec.parseCKNames(ckData)
        print(kekNames)
        
        ckNames = dec.buildCKName(ckName,kekNames)
        print(ckNames)
        
        
        
        
        
        
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

