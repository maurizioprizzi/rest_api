import bcrypt

def encrypt_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def decrypt_password(encrypted_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), encrypted_password)
