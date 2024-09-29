
import os
import socket
import ssl
def generate_new_key(client_ip):
    random_key = os.urandom(32)
    with open ("C:/Users/idan shema/Desktop/projects/keys/{}".format(client_ip), 'wb') as key_file:
        key_file.write(random_key)
    return random_key

def read_current_key(client_ip):
    with open ("C:/Users/idan shema/Desktop/projects/keys/{}".format(client_ip), 'rb') as key_file:
        key = key_file.read()
        return random_key

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1",8080))
sock.listen(1)

print("server is listening")
while True: 
    connection , address = sock.accept()
    ssl_connection= ssl.wrap_socket(connection, server_side=True, certfile="server.cert", keyfile="server.key")
    ip , port = ssl_connection.getpeername()
    random_key = generate_new_key(ip)
    ssl_connection.sendall(random_key)

