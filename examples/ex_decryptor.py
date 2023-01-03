import logging
import os,sys
from typing import Optional
import ndn.utils
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.encoding import *
from nac.encryptor import Encryptor
from nac.decryptor import Decryptor
from nac.tlvmodels import *
from ndn.security import *
from nac.ECIES import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import ECC
from base64 import b64decode, b64encode


logging.basicConfig(format='[{asctime}]{levelname}:{message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    style='{')

amPrefix = '/Alice/Home'
app = NDNApp()

        
async def main():
    basedir = os.path.dirname(os.path.abspath(sys.argv[0]))
    tpm_path = os.path.join(basedir, 'privKeys')
    pib_path = os.path.join(basedir, 'pib.db')
    keychain = KeychainSqlite3(pib_path, TpmFile(tpm_path))
    
    
    dec = Decryptor(amPrefix)

    contentName = '/Home/livingroom/camera/feed/1'
    identity = '/Home/user/Alice/KEY'
    await dec.decode(app,keychain,contentName,identity)


if __name__ == '__main__':
    app.run_forever(after_start=main())

