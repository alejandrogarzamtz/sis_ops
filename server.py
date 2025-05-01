import socket
import threading

HOST = 'localhost'
PORT = 9999
clients = []

def handle(client):
    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                break
            print(f"[CLIENTE]: {msg.decode()}")
            if b"trigger" in msg:
                for c in clients:
                    c.send(b"trigger LIMPIEZA")
        except:
            break
    client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("Servidor listo en puerto 9999... Esperando clientes...")

while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    print(f"[NUEVO CLIENTE CONECTADO] {addr}")
    thread = threading.Thread(target=handle, args=(client_socket,))
    thread.start()
