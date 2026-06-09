import tkinter as tk
import socket
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from login_module.login_interface.tcp_by_size import recv_by_size, send_with_size


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

def encr_prefix(msg):
    return "ENCR"+msg

def noen_prefix(msg):
    return "NOEN"+msg

class LoginClient:
    def __init__(self):
        self.sock = None
        self.secure = None
        self.connected = False
        self.aes_key = None

        self.root = tk.Tk()
        self.root.title("Secure Client")
        self.root.geometry("300x180")

        tk.Label(self.root, text="Username").pack(pady=(15, 5))

        self.entry = tk.Entry(self.root)
        self.entry.pack()

        self.status_label = tk.Label(self.root, text="Starting...")
        self.status_label.pack(pady=5)

        self.response_label = tk.Label(self.root, text="")
        self.response_label.pack()

        self.entry.bind("<Return>", self.send_username)
        self.root.protocol("WM_DELETE_WINDOW", self.disconnect)

        self.root.after(100, self.try_connect)

    def try_connect(self):
        if self.connected:
            return

        try:
            self.sock = socket.socket()
            self.sock.connect(("0.0.0.0", 12345))

            aes_key = AESGCM.generate_key(bit_length=256)

            send_with_size(self.sock, b"RSA")

            rsa_pub = recv_by_size(self.sock)
            rsa_pub = serialization.load_pem_public_key(rsa_pub)

            encrypted_key = rsa_pub.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            send_with_size(self.sock, b"AES\x1E" + encrypted_key)

            self.secure = SecureSession(aes_key)
            self.aes_key = aes_key
            self.connected = True

            self.status_label.config(text="Connected", fg="green")

        except Exception:
            self.sock = None
            self.secure = None
            self.connected = False
            self.status_label.config(text="Not connected... retrying", fg="red")

        self.root.after(2000, self.try_connect)

    def send_username(self, event=None):
        username = self.entry.get().strip()

        if not username:
            self.status_label.config(text="Enter username", fg="red")
            return

        if not self.connected:
            self.status_label.config(text="Connecting...", fg="orange")
            return

        try:
            payload = b"GET_UDP\x1E" + username.encode()
            encrypted = self.secure.encrypt(payload)

            send_with_size(self.sock, encrypted)

            response_enc = recv_by_size(self.sock)
            response = self.secure.decrypt(response_enc).decode()

            parts = response.split("\x1E")

            if parts[0] != "UDP":
                self.response_label.config(text="error")
                return

            ip = parts[1]
            port = int(parts[2])

            self.status_label.config(text="Connecting to game...")

            self.entry.config(state="disabled")

            self.start_game(ip, port)

        except Exception as e:
            self.status_label.config(text=f"Send error: {e}", fg="red")
            self.connected = False
            self.sock = None
            self.secure = None

    def start_game(self, ip, port):
        try:
            if self.sock:
                payload = b"LEAV"
                encrypted = self.secure.encrypt(payload)
                send_with_size(self.sock,encrypted)
                self.sock.close()
        except:
            pass
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.settimeout(3)
        username = self.entry.get().strip()
        msg = noen_prefix(f"CONN\x1E{username}").encode()
        for i in range(5):
            udp_sock.sendto(msg, (ip, port))
            try:
                data, addr = udp_sock.recvfrom(1024)
                try:
                    response = data.decode()
                except:
                    continue

                if response == "OK":
                    print("UDP connected successfully")
                    break

            except socket.timeout:
                print("Retrying UDP...")

        else:
            self.status_label.config(text="UDP failed")
            return

        self.root.destroy()

        from game_module.game.game_code import handle_game
        handle_game((ip, port), self.aes_key, udp_sock)

    def disconnect(self):
        try:
            if self.sock:
                self.sock.close()
        except:
            pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()