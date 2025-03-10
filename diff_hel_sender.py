import socket
from cryptography.fernet import Fernet

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def get_aes_key(dh_key: int, salt: bytes = b"dh-salt") -> bytes:
    key_bytes = dh_key.to_bytes((dh_key.bit_length() + 7) // 8, "big")
    return HKDF(hashes.SHA256(), 32, salt, b"AES").derive(key_bytes)

n = 37
g = 13
print("Public key:", n, g)

print("For sender:")
x = int(input("Enter private key x: "))

k1 = (g**x) % n 

server = socket.socket()
server.bind(("0.0.0.0", 12345))
server.listen(1)
print("Waiting for connection...")
conn, addr = server.accept()
print(f"Connected to {addr}")

conn.send(str(k1).encode())  

k2 = int(conn.recv(1024).decode())  
while k1 != k2:
    k1 = (k2**x) % n  
    conn.send(str(k1).encode())  
    k2 = int(conn.recv(1024).decode()) 

same_key = int(k1)
print("Same key established:", same_key)

aes_key = get_aes_key(same_key)
print("AES Key:", aes_key.hex())
import base64

fernet_key = base64.urlsafe_b64encode(aes_key) 
cipher_suite = Fernet(fernet_key)

text = input("Enter message to encrypt: ")
ciphertext = cipher_suite.encrypt(text.encode())

conn.send(ciphertext)
print("Message sent successfully.")

conn.close()
