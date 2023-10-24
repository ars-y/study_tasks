import hashlib


def hash_key(key_str: str) -> str:
    """Returns hash of the key."""
    return hashlib.sha256(key_str.encode()).hexdigest()
