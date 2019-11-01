import hashlib


def create_md5(password):
    hash_md5 = hashlib.md5()
    hash_md5.update(password.encode('utf-8'))
    return hash_md5.hexdigest()