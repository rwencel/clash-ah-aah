import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def _new_aes(password, iv):
    # This is the recommended cost for bcrypt, higher is more secure but slower
    cost: int = 12

    # This is the salt that bcrypt uses to discourage rainbow attacks, it's not a secret
    # Must be 16 bytes long
    salt: bytes = b'ClashMakesUSalty'
    assert len(salt) == 16

    key: bytes = scrypt(password, salt, key_len=32, N=2**cost, r=AES.block_size, p=1)

    return AES.new(key, AES.MODE_CBC, iv = iv)

def encrypt(unencrypted_text: str, password: str) -> str:
    """Encrypts a string using AES-256-CBC using the password as the key."""

    # Create a random initialization vector using a cryptographically secure algorithm
    iv: bytes = get_random_bytes(AES.block_size)

    aes = _new_aes(password, iv)
    
    # Convert from utf-8 to bytes as aes functions expect
    unencrypted_bytes: bytes = unencrypted_text.encode()

    # and must be a multiple of AES block size per doc
    unencrypted_bytes = pad(unencrypted_bytes, AES.block_size)

    encrypted: bytes = aes.encrypt(unencrypted_bytes)

    # prefix with iv, and base64 encode so we can return a string instead of bytes
    return base64.b64encode(aes.iv + encrypted).decode('utf-8')

def decrypt(encrypted_text: str, password: str) -> str:
    """Decrypts a string using AES-256-CBC using the password as the key."""

    # Convert from string to bytes
    encrypted_bytes: bytes = base64.b64decode(encrypted_text)

    # Extract the initialization vector from the ciphertext
    iv: bytes = encrypted_bytes[:AES.block_size]

    # Remove the IV from the beginning of the ciphertext
    encrypted_bytes = encrypted_bytes[AES.block_size:]

    aes = _new_aes(password, iv)

    decrypted: bytes = aes.decrypt(encrypted_bytes)
    
    # remove any padding
    decrypted = unpad(decrypted, block_size=AES.block_size)

    # convert from bytes to utf-8 string
    return decrypted.decode('utf-8')