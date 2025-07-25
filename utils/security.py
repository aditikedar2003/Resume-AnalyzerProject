import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    if isinstance(hashed, bytes):
        hashed = hashed.decode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
