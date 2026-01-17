from pwdlib import PasswordHash

# Hashing
pwd_hash = PasswordHash.recommended()

class Hash():
    def password_hashing(password: str):
        return pwd_hash.hash(password)
    
    def verify_password(plain_password, hashed_password):
        return pwd_hash.verify(plain_password, hashed_password)