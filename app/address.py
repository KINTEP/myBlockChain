#from block import Block
from keys import PrivateKey, S256Point, N
import random
from helper import hash256, little_endian_to_int, decode_base58

class Keys:
    def __init__(self, secret = None):
        self.secret = secret
        if self.secret == None:
            self.secret = random.randint(1,N)
        else:
            self.secret = secret
        self.key = PrivateKey(little_endian_to_int(hash256(str(self.secret).encode())))

    def getPublicAdress(self):
        address = self.key.point.address(testnet=False)
        return address

    def getPrivateAdress(self):
        p_key = self.key.wif()
        return p_key
        
    def sign(self, z):
        cords = self.key.sign(z)
        return cords.s, cords.r

    def verify(self, z):
        #Private = PrivateKey(secret = e)
        sig = self.key.sign(z)
        print(type(sig))
        r,s = sig.r, sig.s
        point = (self.key.point.x, self.key.point.y)
        px = point[0]
        py = point[1]
        ver = S256Point(px, py)
        return ver.verify(z, sig)


#Lets try the keys class
#document = "This is my talent and God's calling. I stronlgy believ i am going to be the richest man in the whole world before I die"
#z = int.from_bytes(hash256(document.encode()), 'big')
#e = 123676463847

#key = Keys()
#print(key.getPublicAdress())
#print(key.getPrivateAdress())