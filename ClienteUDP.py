import socket
import threading

servidor = ("127.0.0.1", 5001)

def recibir_mensajes(s):
    while True:
        try:
            datos, _ = s.recvfrom(1024)
            print(datos.decode())
        except OSError:
            break
        except Exception as e:
            print(f"\nError {e}")
            break

print("Chat UDP")
nombre = input("Ingresa tu nombre de usuario: ").strip()

if not nombre:
    print("El nombre no debe de estar vacio")
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 0))

try:
    s.sendto(f"/registro {nombre}".encode(), servidor)
    
    respuesta, _ = s.recvfrom(1024)
    mensaje_resp = respuesta.decode()
    
    if "lleno" in mensaje_resp or "uso" in mensaje_resp:
        print(mensaje_resp)
        s.close()
        exit()
        
    print(mensaje_resp)
except Exception as e:
    print(f"Error al contactar al servidor: {e}")
    s.close()
    exit()

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
            print("Saliendo")
            s.close()
            break

        s.sendto(texto.encode(), servidor)

    except KeyboardInterrupt:
        print("\nSaliendo")
        s.close()
        break
    except Exception as e:
        print(f"Error al enviar: {e}")
        s.close()
        break