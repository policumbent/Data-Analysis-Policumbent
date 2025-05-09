from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
os.chdir(os.path.dirname(__file__))

def browse_folder(index):
    folder_selected = filedialog.askdirectory(initialdir="/", title="Seleziona una cartella")
    entries[index].delete(0, END)
    entries[index].insert(0, folder_selected)

def delete_frame(index):
    frames[index].destroy()
    del frames[index]  # Rimuove il riferimento al frame distrutto
    del labels[index]  # Rimuove il riferimento alla label distrutta
    update_numbers()

def update_numbers():
    for i, label in enumerate(labels):
        label.config(text=f"Label {i}")

# Creazione della finestra principale
root = Tk()
root.title("Gestione di Frame e Button")

# Liste per memorizzare le coppie di Frame e Button
frames = []
buttons_delete = []
entries = []
labels = []

# Funzione per creare una nuova coppia di Frame e Button
def create_frame_with_button():
    index = len(frames)  # Indice della nuova coppia
    frame = Frame(root)
    frame.pack(pady=5)

    label = Label(frame, text=f"Label {index}")
    label.pack()
    labels.append(label)

    entry = Entry(frame, width=50)
    entry.pack()
    entries.append(entry)

    button_browse = Button(frame, text="Sfoglia", command=lambda i=index: browse_folder(i))
    button_browse.pack(side=LEFT)

    button_delete = Button(frame, text="Elimina", command=lambda i=index: delete_frame(i))
    button_delete.pack(side=RIGHT)

    frames.append(frame)
    buttons_delete.append(button_delete)

# Creazione del pulsante per aggiungere nuove coppie di Frame e Button
add_button = Button(root, text="Aggiungi Frame e Button", command=create_frame_with_button)
add_button.pack(pady=10)

# Avvio del ciclo principale dell'interfaccia grafica
root.mainloop()