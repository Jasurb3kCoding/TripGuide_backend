from hashlib import sha256, sha512, sha384, md5


def trip_hash(code=None):
    result = sha256(code.encode()).hexdigest()
    result = sha512(result.encode()).hexdigest()
    result = sha384(result.encode()).hexdigest()
    result = md5(result.encode()).hexdigest()
    return result
