import tkinter as tk
import socket

# Crear la ventana
window = tk.Tk()
window.title("Consulta de información")
window.geometry("500x300")

txt_label = tk.Label(window, text="Necesito tu ID para poder consultar tu información")
txt_label2 = tk.Label(window, text="Ejemplo con 17 caracteres: 00100100100000001")
id_label = tk.Label(window, text="ID:")
id_entry = tk.Entry(window)
info_label = tk.Label(window, text="")


def consultar():
    #host y puerto
    HOST = socket.gethostname() # cambiar por una ip real
    PORT = 4444

    # Crear una conexión con el servidor socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect((socket.gethostname(), 4444))
    client_socket.connect((HOST, PORT))

    # Enviar la solicitud al servidor
    id = id_entry.get()
    client_socket.send(id.encode())

    # Recibir la respuesta del servidor
    response = client_socket.recv(1024).decode()

    # Mostrar la información en la etiqueta correspondiente
    info_label.config(text=response)

    # Cerrar la conexión con el servidor
    client_socket.close()

# Crear el botón de consulta
consulta_button = tk.Button(window, text="Consultar", command=consultar)

# Colocar los widgets en la ventana
txt_label.pack()
txt_label2.pack()
id_label.pack()
id_entry.pack()
consulta_button.pack()
info_label.pack()

# Iniciar la ventana
window.mainloop()