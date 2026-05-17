import socket
import threading
from datetime import datetime
from Usuario import Usuario


class ServidorTCP:
    def __init__(self, host, puerto):
        self.host = host
        self.puerto = puerto
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usuarios = []
        self.ejecutando = True

    def iniciar(self):
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servidor.bind((self.host, self.puerto))
        self.servidor.listen(5)
        self.servidor.settimeout(1.0)

        print(f"Servidor TCP escuchando en {self.host}:{self.puerto}")

        print("Presiona Ctrl+C para volver al menú principal.")



        try:
            while self.ejecutando:
                
                try:
                    conexion, direccion = self.servidor.accept()

                    if len(self.usuarios) >= 5:
                        conexion.send("Servidor lleno (máximo 5 usuarios).".encode())
                        conexion.close()
                        hilo.daemon = True
                        hilo = threading.Thread(target=self.registrar_cliente, args=(conexion, direccion))
                        hilo.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[TCP] detenido.")
            
        finally:
            self.detener()

    def registrar_cliente(self, conexion, direccion):
        conexion.send("Ingrese su nombre de usuario: ".encode())
        nombre = conexion.recv(1024).decode().strip()

        for usuario in self.usuarios:
            if usuario.nombre == nombre:
                conexion.send("Nombre ya en uso.".encode())
                conexion.close()
                return

        nuevo_usuario = Usuario(nombre, conexion, direccion)
        self.usuarios.append(nuevo_usuario)

        self.publico(f"{nombre} se ha unido al chat.", None)

        while True:
            try:
                mensaje = conexion.recv(1024).decode()

                if not mensaje:
                    break

                if mensaje.startswith("/privado"):
                    partes = mensaje.split(" ", 2)

                    if len(partes) < 3:
                        conexion.send("Formato: /privado usuario mensaje".encode())
                        continue

                    destinatario = partes[1]
                    contenido = partes[2]

                    self.enviar_privado(nombre, destinatario, contenido)

                else:
                    self.publico(mensaje, nombre)

            except:
                break

        self.desconectar_usuario(nombre)

    def publico(self, mensaje, remitente):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if remitente:
            mensaje_final = f"[{fecha}] {remitente}: {mensaje}"
        else:
            mensaje_final = f"[{fecha}] {mensaje}"

        for usuario in self.usuarios:
            try:
                usuario.conexion.send(mensaje_final.encode())
            except:
                pass

    def enviar_privado(self, remitente, destinatario, mensaje):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        for usuario in self.usuarios:
            if usuario.nombre == destinatario:
                mensaje_final = f"[PRIVADO][{fecha}] {remitente}: {mensaje}"
                usuario.conexion.send(mensaje_final.encode())
                return

    def desconectar_usuario(self, nombre):
        for i in range(len(self.usuarios)):
            if self.usuarios[i].nombre == nombre:
                self.usuarios[i].conexion.close()
                del self.usuarios[i]
                self.publico(f"{nombre} salió del chat.", None)
                break
        
    def detener(self):
            self.ejecutando = False
            for u in self.usuarios:
                u.conexion.close()
            self.servidor.close()
            print("[TCP] Socket cerrado.")    
            
if __name__ == "__main__":
    try:
        servidor = ServidorTCP()
        servidor.iniciar()
    except KeyboardInterrupt:
        print("\nServidor TCP detenido.")
        