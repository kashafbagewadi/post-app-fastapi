from pwdlib import PasswordHash

def hash(password: str):
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def verify(plain_password, hashed_password):
    password_hash = PasswordHash.recommended()
    return password_hash.verify(plain_password, hashed_password)