import socket
import threading

# Configuración centralizada
HOST = "127.0.0.1"
PUERTO_TCP = 5000
PUERTO_UDP = 5001

def recibir_tcp(s):
    """
        Metodo encargado de recibir el apartado tcp
    """
    
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("\n[!] El servidor TCP cerró la conexión.")
                break
            print(f"\n{data.decode()}\n> ", end="")
        except:
            break

def modo_tcp():
    """
        Inicia la conexión de tipo TCP
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PUERTO_TCP))
        print(s.recv(1024).decode(), end="") 
        nombre = input()
        s.send(nombre.encode())
        resp = s.recv(1024).decode()
        print(resp)

        if "uso" in resp or "lleno" in resp:
            return

        threading.Thread(target=recibir_tcp, args=(s,), daemon=True).start()

        while True:
            msg = input("> ")
            if msg == "/salir": break
            s.send(msg.encode())
    except Exception as e:
        print(f"Error conectando a TCP: {e}")
    finally:
        s.close()

def recibir_udp(s):
    """
        Encargada de recibir el apartado UDP
    """
    
    while True:
        try:
            datos, _ = s.recvfrom(1024)
            print(f"\n{datos.decode()}\n> ", end="")
        except:
            break

def modo_udp():
    """
        Inicializa la conexión UDP
    """
    
    servidor_dir = (HOST, PUERTO_UDP)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nombre = input("Nombre para UDP: ")
    
    try:
        s.sendto(f"/registro {nombre}".encode(), servidor_dir)
        s.settimeout(2.0)
        resp, _ = s.recvfrom(1024)
        print(resp.decode())
        s.settimeout(None)

        threading.Thread(target=recibir_udp, args=(s,), daemon=True).start()

        while True:
            msg = input("> ")
            s.sendto(msg.encode(), servidor_dir)
            if msg == "/salir": 
                 break
            
    except Exception as e:
        print(f"Error en UDP: {e}")
    finally:
        s.close()

def menu():
    """
        Modulo de opciones para el cliente.
    """
    
    while True:
        print("\n--- CHAT MULTIPROTOCOLO ---")
        print("1. Entrar modo TCP")
        print("2. Entrar modo UDP")
        print("3. Salir")
        opc = input("Seleccione: ")
        if opc == "1": modo_tcp()
        elif opc == "2": modo_udp()
        elif opc == "3": break

if __name__ == "__main__":
    menu()