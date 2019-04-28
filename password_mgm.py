from passlib.hash import sha256_crypt

salt = "78FHjslS"

def encrypt(password):
    encrypted_password = sha256_crypt.hash(password, salt=salt)
    return encrypted_password

def check(password, encrypted_original):
    return sha256_crypt.verify(password, encrypted_original)