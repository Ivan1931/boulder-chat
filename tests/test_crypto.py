import boulder_chat.crypto as c

def create_test_key():
    return c.create_key('test_key1')

def create_test_string():
    return 'A longish test string'

def test_aes_encryption():
    key = create_test_key()
    test_string = create_test_string()
    assert(c.decrypt_AES(key, c.encrypt_AES(key, test_string)) == test_string)

def test_public_key_encryption():
    key_pair = c.gen_key_RSA()
    public_key = c.export_public_key(key_pair)
    private_key = c.export_private_key(key_pair)
    text = create_test_string()
    decrypted_text = c.decrypt_RSA(c.import_private_key(private_key), c.encrypt_RSA(c.import_public_key(public_key), text))
    assert(text == decrypted_text.decode())
