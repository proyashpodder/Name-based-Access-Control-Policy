from ndn.encoding import *


class NestedModel(TlvModel):
    encryptedPayload = BytesField(0x84)
    initializationVector = BytesField(0x85)
    ckName = NameField()
    

class EncryptedContent(TlvModel):
    inner = ModelField(0x82,NestedModel)
    
    
class KEKListModel(TlvModel):
    list = RepeatedField(BytesField(0x83))


