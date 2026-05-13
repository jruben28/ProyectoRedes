import socket
import threading

def recibir_mensajes(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("\n El servidor se cerró.")
                break
            print(data.decode())
        except ConnectionResetError:
            print("\nSe perdió la conexión con el servidor TCP.")
            break
        except Exception as e:
            print(f"\n[!] Error al recibir mensaje: {e}")
            break 

print("Chat TCP")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(("127.0.0.1", 1060))
except ConnectionRefusedError:
    print("Error: El servidor no está encendido o rechazó la conexión.")
    exit()
except Exception as e:
    print(f"Error inesperado al conectar: {e}")
    exit()


try:
    print(s.recv(1024).decode(), end="")
    nombre = input()
    s.send(nombre.encode())

    resp = s.recv(1024).decode()
except Exception as e:
    print(f"Error al registrar el usuario: {e}")
    s.close()
    exit()

if "uso" in resp or "lleno" in resp:
    print(resp)
    s.close()
    exit()

print(resp)

hilo = threading.Thread(target=recibir_mensajes, args=(s,))
hilo.daemon = True
hilo.start()

print("Comandos: /privado, /salir\n")

while True:
    try:
        texto = input()

        if not texto:
            continue

        if texto == "/salir":
            print("Desconectando")
            s.close()
            break

        s.send(texto.encode())

    except KeyboardInterrupt:
        print("\nSaliendo")
        s.close()
        break
    except Exception as e:
        print(f"Error al enviar: {e}")
        s.close()
        break