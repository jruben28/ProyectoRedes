import socket
from datetime import datetime

HOST = '0.0.0.0'
PORT_UDP = 5001
MAX_USUARIOS = 5

# nombre (ip, puerto)
clientes_udp = {}


def publico_udp(mensaje, remitente_direccion=None):
    """
    Envía mensaje a todos los clientes UDP
    """

    for direccion in clientes_udp.values():

        try:

            # Evitar reenviar al mismo cliente
            if direccion != remitente_direccion:

                servidor_socket.sendto(
                    mensaje.encode(),
                    direccion
                )

        except:
            pass


def enviar_privado_udp(remitente, destinatario, mensaje):
    """
    Envia mensaje privado UDP
    """

    if destinatario in clientes_udp:

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        mensaje_final = (
            f"[PRIVADO][{fecha}] "
            f"{remitente}: {mensaje}"
        )

        try:

            servidor_socket.sendto(
                mensaje_final.encode(),
                clientes_udp[destinatario]
            )

        except:
            pass


def buscar_usuario_por_direccion(direccion):
    """
    Busca nombre usando IP y puerto
    """

    for nombre, dir_cliente in clientes_udp.items():

        if dir_cliente == direccion:
            return nombre

    return None


def servidor_udp():

    global servidor_socket

    # Crear socket UDP
    servidor_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    servidor_socket.bind((HOST, PORT_UDP))

    print(f"Servidor UDP iniciado en puerto {PORT_UDP}")

    while True:

        # Recibir datos
        datos, direccion = servidor_socket.recvfrom(1024)

        mensaje = datos.decode().strip()

        # REGISTRO

        if mensaje.startswith("/registro"):

            partes = mensaje.split(" ", 1)

            if len(partes) < 2:
                continue

            nombre = partes[1]

            # Maximo usuarios
            if len(clientes_udp) >= MAX_USUARIOS:

                servidor_socket.sendto(
                    "Servidor lleno".encode(),
                    direccion
                )

                continue

            # Nombre repetido
            if nombre in clientes_udp:

                servidor_socket.sendto(
                    "Nombre ya en uso".encode(),
                    direccion
                )

                continue

            # Guardar usuario
            clientes_udp[nombre] = direccion

            print(f"{nombre} conectado desde {direccion}")

            servidor_socket.sendto("Bienvenido al chat".encode(), direccion)

            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            publico_udp(
                f"[{fecha}] {nombre} se unio al chat",
                direccion
            )

            continue

        # BUSCAR REMITENTE

        remitente = buscar_usuario_por_direccion(direccion)

        if remitente is None:
            continue

        # MENSAJE PRIVADO

        if mensaje.startswith("/privado"):

            partes = mensaje.split(" ", 2)

            if len(partes) < 3:

                servidor_socket.sendto(
                    "Formato: /privado usuario mensaje".encode(),
                    direccion
                )

                continue

            destinatario = partes[1]
            contenido = partes[2]

            enviar_privado_udp(
                remitente,
                destinatario,
                contenido
            )

        # BROADCAST

        else:

            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            mensaje_final = (
                f"[{fecha}] "
                f"{remitente}: {mensaje}"
            )

            print(mensaje_final)

            publico_udp(
                mensaje_final,
                direccion
            )


if __name__ == "__main__":

    try:
        servidor_udp()

    except KeyboardInterrupt:
        print("\nServidor UDP detenido")