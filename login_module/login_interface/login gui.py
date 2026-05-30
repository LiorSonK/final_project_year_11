import tkinter as tk
import socket
import os

from tcp_by_size import send_with_size, recv_by_size

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

class SecureSession:
    def __init__(self, key):
        self.aesgcm = AESGCM(key)

    def encrypt(self, plaintext):
        nonce = os.urandom(12)
        return nonce + self.aesgcm.encrypt(nonce, plaintext, None)

    def decrypt(self, data):
        nonce = data[:12]
        ciphertext = data[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, None)

sock = None
secure = None
connected = False



def try_connect():
    global sock, secure, connected

    if connected:
        return

    try:
        sock = socket.socket()
        sock.connect(("127.0.0.1", 12345))

        aes_key = AESGCM.generate_key(bit_length=256)

        # start RSA handshake
        send_with_size(sock, b"RSA")

        rsa_pub = recv_by_size(sock)
        rsa_pub = serialization.load_pem_public_key(rsa_pub)

        encrypted_key = rsa_pub.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        send_with_size(sock, b"AES\x1E" + encrypted_key)

        secure = SecureSession(aes_key)
        connected = True

        status_label.config(text="Connected", fg="green")

    except Exception:
        sock = None
        secure = None
        connected = False
        status_label.config(text="Not connected... retrying", fg="red")

    root.after(2000, try_connect)


# ----------------------------
# Send username
# ----------------------------

def send_username(event=None):
    global sock, secure, connected

    username = entry.get().strip()

    if not username:
        status_label.config(text="Enter username", fg="red")
        return

    if not connected:
        status_label.config(text="Connecting first...", fg="orange")
        try_connect()
        root.after(500, lambda: send_username())
        return

    try:
        payload = b"USER\x1E" + username.encode()

        encrypted = secure.encrypt(payload)

        send_with_size(sock, encrypted)

        response_enc = recv_by_size(sock)
        response = secure.decrypt(response_enc).decode()

        response_label.config(text=response)

    except Exception as e:
        status_label.config(text=f"Send error: {e}", fg="red")
        connected = False
        sock = None
        secure = None


# ----------------------------
# Disconnect cleanup
# ----------------------------

def disconnect():
    global sock
    try:
        if sock:
            sock.close()
    except:
        pass
    root.destroy()


# ----------------------------
# UI
# ----------------------------

root = tk.Tk()
root.title("Secure Client")
root.geometry("300x180")

tk.Label(root, text="Username").pack(pady=(15, 5))

entry = tk.Entry(root)
entry.pack()

entry.bind("<Return>", send_username)

status_label = tk.Label(root, text="Starting...")
status_label.pack(pady=5)

response_label = tk.Label(root, text="")
response_label.pack()

root.protocol("WM_DELETE_WINDOW", disconnect)

root.after(100, try_connect)

root.mainloop()