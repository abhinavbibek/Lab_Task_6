import socket
from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def get_aes_key(dh_key: int, salt: bytes = b"dh-salt") -> bytes:
    key_bytes = dh_key.to_bytes((dh_key.bit_length() + 7) // 8, "big")
    return HKDF(hashes.SHA256(), 32, salt, b"AES").derive(key_bytes)

n = 37
g = 13

print("For receiver:")
y = int(input("Enter private key y: "))

k2 = (g**y) % n 

client = socket.socket()
client.connect(("10.1.175.187", 12345))  

k1 = int(client.recv(1024).decode()) 
client.send(str(k2).encode())  

while k1 != k2:
    k2 = (k1**y) % n  
    client.send(str(k2).encode()) 
    k1 = int(client.recv(1024).decode()) 

same_key = int(k1)
print("Same key established:", same_key)

aes_key = get_aes_key(same_key)
print("AES Key:", aes_key.hex())

import base64

fernet_key = base64.urlsafe_b64encode(aes_key) 
cipher_suite = Fernet(fernet_key)

ciphertext = client.recv(1024)  
plaintext = cipher_suite.decrypt(ciphertext).decode()

print("Decrypted message:", plaintext)

client.close()
