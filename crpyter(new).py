from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, GT, pair

class BonehBoyenIBE:
    def __init__(self, groupObj):
        self.group = groupObj
        self.g = self.group.random(G1)

    def setup(self):
        s = self.group.random(ZR) 
        public_params = self.g ** s
        return s, public_params

    def extract(self, master_key, ID):
        q_ID = self.group.hash(ID, G1)
        d_ID = q_ID ** master_key
        return d_ID

    def encrypt(self, public_params, ID, message):
        q_ID = self.group.hash(ID, G1)
        r = self.group.random(ZR)
        g_r = self.g ** r
        c1 = g_r
        h_ID_r = pair(q_ID, public_params ** r)
        c2 = message * h_ID_r
        return (c1, c2)

    def decrypt(self, private_key, ciphertext):
        c1, c2 = ciphertext
        m = c2 / pair(c1, private_key)
        return m

groupObj = PairingGroup('SS512')
ibe = BonehBoyenIBE(groupObj)
s, public_params = ibe.setup()
ID = "user@example.com"
message = groupObj.random(GT)
print("Original message:", message)

d_ID = ibe.extract(s, ID)
ciphertext = ibe.encrypt(public_params, ID, message)
print("Encrypted:", ciphertext)

decrypted_message = ibe.decrypt(d_ID, ciphertext)
print("Decrypted message:", decrypted_message)

assert message == decrypted_message, "The decrypted message does not match the original message."

