import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Secret key for AES-256 encryption (32 bytes)
SECRET_KEY = hashlib.sha256(b"CodeAlpha_SecretKey_2026").digest()

def encrypt_data(plain_text):
    """Encrypts sensitive data using AES-256"""
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    # Combine IV + encrypted data and encode to base64
    result = base64.b64encode(cipher.iv + encrypted).decode('utf-8')
    return result

def decrypt_data(encrypted_text):
    """Decrypts AES-256 encrypted data"""
    raw = base64.b64decode(encrypted_text)
    iv = raw[:16]
    encrypted = raw[16:]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode('utf-8')

def hash_password(password):
    """Hashes a password using SHA-256 (one-way, for login verification)"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()