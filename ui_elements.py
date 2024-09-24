import tkinter as tk


def create_taped_label(parent, text):
    # Crear el Label con estilo de papel
    label_frame = tk.Frame(parent, bg="#F5DEB3", bd=2, relief="ridge")  # Fondo color papel, borde simulado

    # Crear el texto dentro del "papel"
    label = tk.Label(label_frame, text=text, font=("Baskerville old Face", 13), bg="#F5DEB3")
    label.pack(padx=10, pady=5)
    return label_frame
