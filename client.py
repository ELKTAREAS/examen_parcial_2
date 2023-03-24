import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import socket


# Crear la ventana
window = tk.Tk()
window.title("Consulta de información")
window.geometry("600x300")

# Crear el estilo
style = ThemedStyle(window)
style.set_theme("arc")

# Colocar los widgets en la ventana
txt_label = ttk.Label(window, text="Necesito tu ID para poder consultar tu información", font=("Arial", 16))
txt_label2 = ttk.Label(window, text="Ejemplo con 17 caracteres: 00100100100000001")
id_label = ttk.Label(window, text="ID:")
id_entry = ttk.Entry(window, width=35)
info_label = ttk.Label(window, text="")

def consultar():
    #host y puerto
    HOST = '192.168.229.136' # cambiar por una ip real
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

txt_label.pack()
txt_label2.pack()
id_label.pack()
id_entry.pack()
consulta_button.pack()
info_label.pack()

# Iniciar la ventana
window.mainloop()


# Path: server_exam.py