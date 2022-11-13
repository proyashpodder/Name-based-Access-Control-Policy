# -----------------------------------------------------------------------------
# Copyright (C) 2019-2020 The python-ndn authors
#
# This file is part of python-ndn.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------
import logging
import sys
from typing import Optional
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import *
from encryptor import Encryptor
from tlvmodels import KEKListModel


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

amPrefix = '/Alice/Home'
app = NDNApp()

        
async def main():
    try:
        data_to_encrypt = 'hello world'
        contentName = '/Home/livingroom/camera/feed/1'
        schema = sys.argv[1]
        
        
        enc = Encryptor(amPrefix)
        dic = enc.parseSchema(schema)
        print(dic)
        
        KekNames = enc.getKEKName(dic,Name.from_str(contentName))
        print(KekNames)
        
        #build the Interest name to fetch the name of the KEK(s) needed to encrypt the CK
        '''keklistName = enc.buildKeklistName(contentName)
        
        
        #kekList = fetchKEKNames('/Alice/Home/NAC/KEKList/Home/livingroom/_/_/CK')
        #ckName = '/Alice/Home/NAC/KEKList/Home/livingroom/_/_/CK'
        
        # send the Interest to fetch KEK names
        name = Name.from_str(keklistName)
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, kekList = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
    
        
        # parse the KEK names
        KekNames = enc.parseKEKNames(bytes(kekList))'''
        keks = {}
        
        # Send Interest to fetch KEK(s).
        for KekName in KekNames:
            print(f'Sending Interest {Name.to_str(KekName)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, kek = await app.express_interest(
                KekName, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(kek) if kek else None)
            keks[KekName] = kek

        
        #encrypt content with CK
        ck, encryptedContent = enc.encrypt_content(data_to_encrypt.encode())
        print(keks)
        enc.publishCKNames(app,contentName,keks)
        #publish CK and Content
        enc.publishCK(app,contentName,ck,keks)
        enc.publishContent(app,contentName,encryptedContent)
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
