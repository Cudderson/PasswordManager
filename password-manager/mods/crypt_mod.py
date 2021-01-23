from cryptography.fernet import Fernet


def encrypt_password(pass_to_encrypt):
    """Encrypts and returns the passed value as a Fernet token"""

    temp_key = get_crypt_key()
    tk = Fernet(temp_key)

    pass_to_encrypt = pass_to_encrypt.encode("UTF-8")
    return tk.encrypt(pass_to_encrypt)


def decrypt_password(pass_to_decrypt):
    """Decrypts and returns the passed value for the user to read"""

    pass_to_decrypt = fk.decrypt(pass_to_decrypt)
    return pass_to_decrypt.decode()