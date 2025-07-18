import json
import base64
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# FUNCIONES DE COMPATIBILIDAD CON CRYPTOJS

def derive_key_and_iv(password, salt, key_length, iv_length):
    """Deriva la clave y el IV igual que CryptoJS (OpenSSL EVP_BytesToKey)"""
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = hashlib.md5(d_i + password.encode('utf-8') + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def cryptojs_encrypt(plaintext, password):
    bs = AES.block_size
    salt = get_random_bytes(8)
    key, iv = derive_key_and_iv(password, salt, 32, 16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padding_len = bs - len(plaintext.encode('utf-8')) % bs
    padded = plaintext + chr(padding_len) * padding_len
    ciphertext = cipher.encrypt(padded.encode('utf-8'))
    # Formato compatible con CryptoJS: Salted__ + salt + ciphertext, todo en base64
    encrypted = b"Salted__" + salt + ciphertext
    return base64.b64encode(encrypted).decode('utf-8')

def encrypt_field(value, password):
    if isinstance(value, str):
        return cryptojs_encrypt(value, password)
    if isinstance(value, list):
        return [encrypt_field(v, password) for v in value]
    if isinstance(value, dict):
        return {k: encrypt_field(v, password) for k, v in value.items()}
    return value

def main():
    if len(sys.argv) != 4:
        print("Uso: python encrypt_tasks_compatible.py tasks.json encrypted.json TUCONTRASENA")
        sys.exit(1)
    tasks_path = sys.argv[1]
    encrypted_path = sys.argv[2]
    password = sys.argv[3]

    with open(tasks_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    encrypted_tasks = []
    for task in tasks:
        enc_task = {}
        for k, v in task.items():
            if k in ('original', 'answers', 'keyword', 'prompt', 'tags'):
                enc_task[k] = encrypt_field(v, password)
            else:
                enc_task[k] = v
        encrypted_tasks.append(enc_task)

    with open(encrypted_path, 'w', encoding='utf-8') as f:
        json.dump(encrypted_tasks, f, indent=2, ensure_ascii=False)

    print(f"Archivo cifrado generado: {encrypted_path}")

if __name__ == "__main__":
    main()