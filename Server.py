import socket
import threading
import json


HOST = '0.0.0.0'
PORT_TCP = 5000
PORT_UDP = 5001
MAX_USUARIOS = 5


# DICCIONARIO para mapear nombre y socket
clientes_conectados = {} 
direcciones = set()

def broadcast_tcp(mensaje, remitente_socket):
    """Envía a todos los conectados vpia tcp."""
    
    

def broadcast_udp(mensaje, remitente_socket):
    """Envía a todos los conecatdos vía udp."""
    

def manejar_cliente(cliente_socket, direccion):
    """  """
    print()


def servidor_tcp():
    # Inicializar server tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT_TCP))
    server_socket.listen(1)

    print("--- Servidor TCP inicializado ---")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    while True:
        data = conn.recv(1024)
        if not data: break
        conn.sendall(data)
    conn.close()
    
    
def servidor_udp():
    #Inicializar server UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT_UDP))

    print("--- Servidor UDP inicializado ---")
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received from {addr}: {data.decode()}")
        server_socket.sendto(b"ACK", addr)
    


def iniciar_aplicacion():
    
    # interfaz gráfica(?)
    
    
    
    

if __name__ == "__main__":
    try:
        iniciar_aplicacion()
    except KeyboardInterrupt:
        print("\nServidor detenido.")