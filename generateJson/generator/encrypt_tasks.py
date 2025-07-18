import json
import base64
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

def pad(text):
    pad_len = 16 - (len(text) % 16)
    return text + chr(pad_len) * pad_len

def unpad(text):
    pad_len = ord(text[-1])
    return text[:-pad_len]

def aes_encrypt(plain_text, key):
    # IV para cada campo (seguridad extra)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(plain_text).encode('utf-8'))
    # Guardamos IV+ciphertext juntos, ambos en base64
    return base64.b64encode(iv + ct_bytes).decode('utf-8')

def encrypt_field(value, key):
    if isinstance(value, str):
        return aes_encrypt(value, key)
    if isinstance(value, list):
        return [encrypt_field(v, key) for v in value]
    if isinstance(value, dict):
        return {k: encrypt_field(v, key) for k, v in value.items()}
    return value

def main():
    if len(sys.argv) != 4:
        print("Uso: python encrypt_tasks.py tasks.json encrypted.json TUCONTRASENA")
        sys.exit(1)
    tasks_path = sys.argv[1]
    encrypted_path = sys.argv[2]
    password = sys.argv[3]

    # Derivar clave desde la contraseña con un salt fijo (puedes cambiarlo por uno mejor)
    salt = b'some_salt_for_tasks'  # Puedes usar un salt fijo, o guardarlo y compartirlo con el descifrado
    key = PBKDF2(password, salt, dkLen=32, count=100_000)

    with open(tasks_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    encrypted_tasks = []
    for task in tasks:
        enc_task = {}
        for k, v in task.items():
            # Solo ciframos los campos sensibles
            if k in ('original', 'answers', 'keyword', 'prompt', 'tags'):
                enc_task[k] = encrypt_field(v, key)
            else:
                enc_task[k] = v
        encrypted_tasks.append(enc_task)

    with open(encrypted_path, 'w', encoding='utf-8') as f:
        json.dump(encrypted_tasks, f, indent=2, ensure_ascii=False)

    print(f"Archivo cifrado generado: {encrypted_path}")

if __name__ == "__main__":
    main()
