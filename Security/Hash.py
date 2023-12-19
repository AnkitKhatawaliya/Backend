import hashlib


def Convert_to_hash(password: str):
    password = "goat" + password + "doge"
    hash_object = hashlib.sha256()
    hash_object.update(password.encode('utf-8'))
    hashed_password = hash_object.hexdigest()
    return hashed_password
