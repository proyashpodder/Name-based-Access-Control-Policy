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
        contentName = '/Home/livingroom'
        
        enc = Encryptor(amPrefix)
        
        keklistName = enc.buildKeklistName(contentName)
        
        
        #kekList = fetchKEKNames('/Alice/Home/NAC/KEKList/Home/livingroom/_/_/CK')
        #ckName = '/Alice/Home/NAC/KEKList/Home/livingroom/_/_/CK'
        
        name = Name.from_str(keklistName)
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, kekList = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
    
        
        KekNames = enc.parseKEKNames(bytes(kekList))
        keks = {}
        for KekName in KekNames:
            print(f'Sending Interest {Name.to_str(KekName)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
            data_name, meta_info, kek = await app.express_interest(
                KekName, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(kek) if kek else None)
            keks[KekName] = kek

        
        ck, encryptedContent = enc.encrypt_content(data_to_encrypt.encode())
        #print(ck, encryptedContent)
        #ckNames = enc.buildckName(contentName)
        #for kek in keks:
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
