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
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import *
from encryptor import Encryptor


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')


app = NDNApp()



class KEKListModel(TlvModel):
    list = RepeatedField(BytesField(0x83))


async def main():
    try:
        timestamp = ndn.utils.timestamp()
        amPrefix = '/Alice/Home'
        name = Name.from_str('/Alice/Home/NAC/KEKList/Home/livingroom/_/_/CK')
        #+ [Component.from_timestamp(timestamp)]
        print(f'Sending Interest {Name.to_str(name)}, {InterestParam(must_be_fresh=True, lifetime=6000)}')
        data_name, meta_info, content = await app.express_interest(
            name, must_be_fresh=True, can_be_prefix=False, lifetime=6000)

        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        print(bytes(content) if content else None)
        
        enc = Encryptor(amPrefix)
        encryptedContent = enc.encrypt_content('hola'.encode())
        
        KekNames = enc.parseKEKNames(bytes(content))
        for KekName in KekNames:
            print(KekName)
            data_name, meta_info, content = await app.express_interest(
                KekName, must_be_fresh=True, can_be_prefix=False, lifetime=6000)
        #model = KEKListModel.parse(bytes(content))
        #print(model.list)
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
