from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# from run import *
import os
os.chdir(os.path.dirname(__file__))



def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

root = Tk()
root.title("Finestra con Scorrimento")

# Creazione di una finestra scorrevole con un Canvas e barre di scorrimento
scrollbar_y = Scrollbar(root, orient="vertical")
scrollbar_y.pack(side="right", fill="y")

canvas = Canvas(root, yscrollcommand=scrollbar_y.set)
canvas.pack(side="left", fill="both", expand=True)

scrollbar_y.config(command=canvas.yview)

# Aggiungere il tuo contenuto al canvas
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Aggiungere molti widget (ad esempio, etichette, pulsanti, ecc.) al frame
for i in range(50):
    label = Label(frame, text=f"Elemento {i}")
    label.pack(pady=5)

# Configurare il canvas per scorrere quando necessario
frame.bind("<Configure>", on_configure)

root.mainloop()




# def toggle_selezione(*args):
#     clicked_value = var.get()
    
#     if clicked_value == last_selected.get():
#         var.set(None)  # Deseleziona il pulsante corrente
#     else:
#         last_selected.set(clicked_value)

# root = Tk()

# var = StringVar()
# last_selected = StringVar(value="")  # Variabile di tracciamento per tenere traccia dell'ultimo pulsante selezionato

# rb1 = Radiobutton(root, text="Opzione 1", variable=var, value="opzione1")
# rb2 = Radiobutton(root, text="Opzione 2", variable=var, value="opzione2")
# rb3 = Radiobutton(root, text="Opzione 3", variable=var, value="opzione3")

# # Collega la funzione toggle_selezione alla variabile di tracciamento
# var.trace_add("write", toggle_selezione)

# rb1.pack()
# rb2.pack()
# rb3.pack()

# root.mainloop()



# # # def show_selected():
# # #     selected_values = [value.get() for value in checkbutton_vars if value.get() == 1]
# # #     selection_label.config(text=f"Scelte: {', '.join(selected_values)}")

# # def show_selected():
# #     selected_values = get_selected_values()
# #     selection_label.config(text=f"Scelte: {', '.join(selected_values)}")

# # def get_selected_values():
# #     return [str(i + 1) for i, var in enumerate(checkbutton_vars) if var.get() != 0]


# # # def update_label(*args):
# # #     selected_values = [str(i+1) for i, var in enumerate(checkbutton_vars) if var.get() != 0]
# # #     selection_label.config(text=f"Scelte: {', '.join(selected_values)}")

# # # def show_selected():
# # #     selected_values = [str(i+1) for i, var in enumerate(checkbutton_vars) if var.get() != 0]
# # #     selection_label.config(text=f"Scelte: {', '.join(selected_values)}")
    
# # # def updateSelection():
# # #     selected_values = [value.get() for value in checkbutton_vars if value.get() == 1]
# # #     selection_label.config(text=f"Scelte: {', '.join(selected_values)}")    

# # # Creazione della finestra principale
# # root = Tk()
# # root.title("Esempio di Checkbutton")

# # # Variabili di controllo per i Checkbutton

# # checkbutton_vars = []
# # index_list = ["timestamp","altitude","heart_rate","cadence","distance","speed","power","RPMw_bo_RPMp","ideal_speed","gear"]
# # # checkbutton_vars = [StringVar() for _ in range(len(index_list))]

# # selection_label = ttk.Label(root, text="Scelte: ")

# # # Creazione dei Checkbutton
# # for i in range(len(index_list)):
# #     var = IntVar()
# #     checkbutton = (ttk.Checkbutton(root, text=index_list[i], variable=var, command=lambda: show_selected(selection_label)))
# #     checkbutton.pack(anchor=W)
# #     checkbutton_vars.append(var)
    
# # # for var in checkbutton_vars:
# # #     var.trace_add("write", update_label)
    
# # # Etichetta per visualizzare le scelte
# # selection_label.pack(pady=10)

# # # Avvio del ciclo principale dell'interfaccia grafica
# # root.mainloop()













# # def show_selected(selection_label):
# #     selected_values = get_selected_values()
# #     selection_label.config(text=f"Scelte: {', '.join(selected_values)}")

# # def get_selected_values():
# #     return [index_list[i] for i, var in enumerate(checkbutton_vars) if var.get() != 0] #[str(i + 1) for i, var in enumerate(checkbutton_vars) if var.get() != 0]

# # # Creazione della finestra principale
# # root = Tk()
# # root.title("Esempio di Checkbutton")

# # # Lista per memorizzare le variabili di controllo per i Checkbutton
# # checkbutton_vars = []
# # index_list = ["timestamp","altitude","heart_rate","cadence","distance","speed","power","RPMw_bo_RPMp","ideal_speed","gear"]

# # # Etichetta per visualizzare le scelte
# # selection_label = Label(root, text="Scelte: ")
# # selection_label.pack(pady=10)

# # # Creazione dei Checkbutton
# # for i in range(len(index_list)):
# #     var = IntVar()
# #     checkbutton = ttk.Checkbutton(root, text=index_list[i], variable=var, command=lambda: show_selected(selection_label))
# #     checkbutton.pack(anchor=W)
# #     checkbutton_vars.append(var)

# # # Avvio del ciclo principale dell'interfaccia grafica
# # root.mainloop()





