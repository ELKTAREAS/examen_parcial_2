import socket
import threading
# import datetime
# from datetime import datetime
import mysql.connector

# Conexion
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="examen_parcial_bd"
)
# Ejecutante de la base de datos
cursor = db.cursor()

# host y puerto
HOST = '192.168.229.136'
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
    print(f"Solicitud recibida: {data}")

    # Dividir el ID en 4 secciones
    # Usaremos una lista de 4 elementos que contenga los 3 primeros caracteres del ID y el resto de caracteres del ID en el último elemento
    # Por ejemplo, si el ID es 001001001 y cada elemento será un argumento para la consulta SQL que se ejecutará más adelante en el código
    #id = [data[i:i + 3] for i in range(0, 9, 3)]
    id_pais = str(data[0:3])
    cod_zona = str(data[3:6])
    cod_distrito = str(data[6:9])
    id_num = str(data[9:])

    # Consultar la base de datos MySQL para obtener la información del ID recibido del cliente
    cursor.execute(
        f"SELECT pais, zona, distrito FROM distrito D JOIN pais ON pais.codpais = {id_pais} JOIN zona ON zona.codzona = {cod_zona} AND zona.codpais = {id_pais} WHERE D.codpais = {id_pais} AND D.codzona = {cod_zona} AND D.cod_distrito = {cod_distrito}")
    result = cursor.fetchone()

    if result:
        # Si se encontró un resultado, enviar la información al cliente
        response = f"Usted pertenece al pais de {result[0]} de la zona {result[1]} y del distrito {result[2]}"
        client_socket.send(response.encode())

        # Guardar en la bitácora
        cursor.execute(
            "INSERT INTO bitacora (cod_bitacora, codpais, codzona, cod_distrito, fecha) VALUES (%s, %s, %s, %s, NOW())",
            (id_num, id_pais, cod_zona, cod_distrito))
        db.commit()

        # Imprimir la respuesta en el servidor
        print(response)

        # Imprimir la respuesta de la bitacora en el servidor
        cursor.execute("SELECT cod_bitacora, codpais, codzona, cod_distrito, fecha FROM bitacora ORDER BY id DESC LIMIT 1")
        bita = cursor.fetchall()

        # Imprimir la respuesta de la bitacora en el servidor
        print(f"Se ha guardado en la bitacora el ID: {bita[0][0]} del pais: 00{bita[0][1]} de la zona: 00{bita[0][2]} del distrito: 00{bita[0][3]} en la fecha: {bita[0][4]}")

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