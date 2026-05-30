import socket
import threading

from tcp_by_size import send_with_size, recv_by_size

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

import os


class SecureSession:
    def __init__(self, key):
        self.aesgcm = AESGCM(key)

    def encrypt(self, plaintext):
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext, None)
        return nonce + ciphertext

    def decrypt(self, data):
        nonce = data[:12]
        ciphertext = data[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, None)


def load_or_create_keys():
    try:
        with open("private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=b"mypassword",
                backend=default_backend()
            )
        with open("public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        print("Keys loaded")
    except FileNotFoundError:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        with open("private_key.pem", "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.BestAvailableEncryption(
                        b"mypassword"
                    )
                )
            )
        with open("public_key.pem", "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )
        print("Keys generated")

    return private_key, public_key


def handle_client(cli_sock):
    try:
        exchange_method = recv_by_size(cli_sock)
        if exchange_method != b"RSA":
            cli_sock.close()
            return
        send_with_size(
            cli_sock,
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
        aes_message = recv_by_size(cli_sock)
        separator = aes_message.index(b"\x1E")
        encrypted_aes_key = aes_message[separator + 1:]
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        session = SecureSession(aes_key)
        encrypted_data = recv_by_size(cli_sock)
        data = session.decrypt(encrypted_data).decode()
        parts = data.split("\x1E")
        if parts[0] == "USER":
            username = parts[1]
            print("User connected:", username)
            response = f"Hello {username}".encode()
            send_with_size(
                cli_sock,
                session.encrypt(response)
            )
        cli_sock.close()
    except Exception as e:
        print("Client error:", e)
        cli_sock.close()


private_key, public_key = load_or_create_keys()

srv_sock = socket.socket()
srv_sock.bind(("0.0.0.0", 12345))
srv_sock.listen()

print("Server listening on port 12345")

while True:

    client_socket, addr = srv_sock.accept()

    print("Connection from", addr)

    threading.Thread(target=handle_client,args=(client_socket,),daemon=True).start()