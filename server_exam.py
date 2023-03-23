import socket
import threading
# import datetime
# from datetime import datetime
import mysql.connector

# Conexion
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sonaguera0208",
    database="examen_parcial_bd"
)
# Ejecutante de la base de datos
cursor = db.cursor()

# host y puerto
HOST = socket.gethostname()  # cambiar por una ip real
PORT = 4444

# Crear un socket server en el puerto 4444
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((socket.gethostname(), 4444))
server_socket.bind((HOST, PORT))
server_socket.listen(10)  # Hasta 10 clientes
print(f"Servidor en linea en {HOST}:{PORT}...")


# Función que procesa las solicitudes de los clientes
def handle_client(client_socket, client_address):
    print(f"Nueva conexión de {client_address}")

    # Recibir la solicitud del cliente
    data = client_socket.recv(1024).decode()
    """cod_pais = data[:3]
    cod_zona = data[3:6]
    cod_distrito = data[6:9]"""
    id_num = str(data[9:])

    # Dividir el ID en 4 secciones
    # Usaremos una lista de 4 elementos que contenga los 3 primeros caracteres del ID y el resto de caracteres del ID en el último elemento
    # Por ejemplo, si el ID es 12345678900000001, la lista será ["001", "001", "001", "00000001"] y
    # cada elemento será un argumento para la consulta SQL que se ejecutará más adelante en el código
    id = [data[i:i + 3] for i in range(0, 9, 3)]

    # Consultar la base de datos MySQL para obtener la información del ID recibido del cliente
    cursor.execute(
        f"SELECT pais, zona, distrito FROM distrito D JOIN pais ON pais.codpais = {id[0]} JOIN zona ON zona.codzona = {id[1]} AND zona.codpais = {id[0]} WHERE D.codpais = {id[0]} AND D.codzona = {id[1]} AND D.cod_distrito = {id[2]}")
    result = cursor.fetchone()

    if result:
        # Si se encontró un resultado, enviar la información al cliente
        response = f"Usted pertenece al pais de {result[0]} de la zona {result[1]} y del distrito {result[2]}"
        client_socket.send(response.encode())

        # Guardar en la bitácora
        cursor.execute(
            "INSERT INTO bitacora (cod_bitacora, codpais, codzona, cod_distrito, fecha) VALUES (%s, %s, %s, %s, NOW())",
            (id_num, id[0], id[1], id[2]))
        db.commit()

        print(response)
    else:
        # Si no se encontró un resultado, enviar un mensaje de error al cliente
        error_message = "No se encontró información para el ID especificado"
        client_socket.send(error_message.encode())

    # Cerrar la conexión con el cliente
    client_socket.close()
    print(f"Conexión cerrada con {client_address}")


# Esperar conexiones de los clientes
# Cada vez que un cliente se conecte, se creará un nuevo hilo para manejar la solicitud
# del cliente y el servidor seguirá escuchando nuevas conexiones
# Esto permite que el servidor pueda manejar múltiples solicitudes de clientes al mismo
# tiempo y no se quede esperando a que un cliente termine su solicitud
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

# Path: client_exam.py