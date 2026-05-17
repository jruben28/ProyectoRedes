import sys
from ServidorTCP import ServidorTCP
from ServidorUDP import servidor_udp


def menu():
    print("\n--- PANEL DE CONTROL DEL SERVIDOR ---")
    print("1. Iniciar Servidor TCP")
    print("2. Iniciar Servidor UDP")
    print("3. Salir")
    return input("Seleccione una opción: ")

def ejecutar_servidor():
    HOST = "127.0.0.1"
    PUERTO_TCP = 5000
    PUERTO_UDP = 5001

    while True:
        opcion = menu()

        if opcion == "1":
            print(f"\n[SISTEMA] Cambiando a TCP en {HOST}:{PUERTO_TCP}...")
            try:
                servidor = ServidorTCP(host=HOST, puerto=PUERTO_TCP)
                servidor.servidor.settimeout(1.0)
                servidor.iniciar() 
            except KeyboardInterrupt:
                print("\n[SISTEMA] Servidor TCP detenido manualmente.")
            except Exception as e:
                print(f"[ERROR TCP] {e}")

        elif opcion == "2":
            print(f"\n[SISTEMA] Cambiando a UDP en {HOST}:{PUERTO_UDP}...")
            try:
                servidor_udp(host=HOST, puerto=PUERTO_UDP)
            except KeyboardInterrupt:
                print("\n[SISTEMA] Servidor UDP detenido manualmente.")
            except Exception as e:
                print(f"[ERROR UDP] {e}")

        elif opcion == "3":
            print("Saliendo del sistema...")
            sys.exit()
        else:
            print("Opción no válida.")

    


if __name__ == "__main__":
    ejecutar_servidor()
    
    
