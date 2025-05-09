'''
TO READ:

If you want to try/use interface
please run "GUI_free.py" INSTEAD OF "GUI.py"
Just for safety :)
'''

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from run import *
import os
import util
os.chdir(os.path.dirname(__file__))

initialdir_file = util.dtset_path
initialdir_cond = util.dtsettings_path   #"../Dataset/couples"

opts_filt_list = ["rough","medium","extra","no filter"]


def browseFile(entry, initialdir=os.getcwd()):
    file_selected = filedialog.askopenfilename(initialdir=initialdir, title="Select file")   #, filetypes=(("Text files", "*.csv"), ("all files", "*.*")))
    entry.delete(0, END)  # Cancella il contenuto attuale della casella di inserimento
    entry.insert(0, file_selected)  # Inserisce il percorso del file nella casella di inserimento
    
def browseFolder(entry, initialdir="/"):
    folder_selected = filedialog.askdirectory(initialdir=initialdir, title="Select folder")
    entry.delete(0, END)
    entry.insert(0, folder_selected)

def generateEntry(frame, text, initialdir, countgrid, entry_list, folder=False):
    label = ttk.Label(frame, text=text+" (path):")
    label.grid(row=countgrid, column=0, padx=5, pady=5) #, sticky=NSEW)
    # label.place(relx=0.01,rely=countgrid,anchor=W)
    # Get the file path
    file_path = StringVar()
    entry_file = ttk.Entry(frame, width=50, textvariable=file_path)
    entry_file.grid(row=countgrid, column=1, padx=5, pady=5) #, sticky=NSEW)
    # entry_file.place(relx=0.5,rely=countgrid,anchor=CENTER)
    entry_list.append(entry_file)
    # Create a button to select a file
    if folder==False:
        command = lambda: browseFile(entry_file,initialdir)
    else:
        command = lambda: browseFolder(entry_file,initialdir)
    browse_button = ttk.Button(frame, text="Browse", command=command)
    browse_button.grid(row=countgrid, column=2, padx=5, pady=5) #, sticky=NSEW)
    # browse_button.place(relx=0.99,rely=countgrid,anchor=E)
    return file_path

def clear_entries(entry_list):
    for entry in entry_list:
        entry.delete(0, END)
        
def nextRun(analysis,file_path,cond_file_path,folder_path,cond_folder_path,entry_list):
    if len(folder_path.get()) != 0:
        analysis.uploadFolder(folder_path=folder_path.get(),settings_file=cond_folder_path.get())
    else:
        if analysis.settings is not None and cond_file_path.get()=='':
            pass
        else:
            analysis.addSettings(cond_file_path.get())
        analysis.addRun(file_name=file_path.get()) #,cond_file=cond_file_path.get())
    clear_entries(entry_list)

def toggle_frame(frame_index):
    clear_entries(entry_list)
    for i, frame in enumerate(frame_list):
        if i == frame_index:
            frame.grid(row=0, column=1, padx=10, pady=10)
            # frame.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.5, anchor=CENTER)
        else:
            frame.grid_forget()

def update_numbers():
    global label_list
    for i, label in enumerate(label_list):
        label.config(text=f"Plot {i}")

def delete_frame(frame, index):
    frame.destroy()
    global frame_list, label_list, checkbutton_vars_list
    del frame_list[index]  # Rimuove il riferimento al frame distrutto
    del label_list[index]  # Rimuove il riferimento alla label distrutta
    del checkbutton_vars_list[index]
    update_numbers()

def show_selected(selection_label,index):
    selected_values = get_selected_values(index)
    selection_label.config(text=f"Scelte: {', '.join(selected_values)}")

def get_selected_values(index):
    global index_list, checkbutton_vars_list
    return [index_list[i] for i, var in enumerate(checkbutton_vars_list[index]) if var.get() != 0] #[str(i + 1) for i, var in enumerate(checkbutton_vars) if var.get() != 0]

def selectRun(root):
    # Etichetta per visualizzare le scelte
    selection_label = ttk.Label(root, text="Scelte: ")
    # selection_label.pack(pady=10)
    selection_label.grid(row=1,column=0)
    
    global select_run_list

    # Creazione dei Checkbutton
    for i, run in enumerate(analysis.run_list.keys()):
        var = IntVar()
        checkbutton = ttk.Checkbutton(root, text=run, variable=var) #, command=lambda: show_selected(selection_label,index))
        # checkbutton.pack(anchor=W)
        checkbutton.grid(row=int(i/3)+2,column=i%3)
        # checkbutton.pack(pady=5)
        select_run_list.append(var)

# Funzione per creare una nuova coppia di Frame e Button
def create_frame_with_button(root):
    global frame_list
    index = len(frame_list)  # Indice della nuova coppia
    frame = Frame(root)
    frame.pack(pady=5)

    label = ttk.Label(frame, text=f"Plot {index}")
    # label.pack()
    label.grid(row=0,column=0)
    label_list.append(label)
    
    global checkbutton_vars, checkbutton_vars_list
    checkbutton_vars = []
    
    # Etichetta per visualizzare le scelte
    selection_label = ttk.Label(frame, text="Scelte: ")
    # selection_label.pack(pady=10)
    selection_label.grid(row=1,column=0)

    # Creazione dei Checkbutton
    for i in range(len(index_list)):
        var = IntVar()
        checkbutton = ttk.Checkbutton(frame, text=index_list[i], variable=var, command=lambda: show_selected(selection_label,index))
        # checkbutton.pack(anchor=W)
        checkbutton.grid(row=int(i/4)+2,column=i)
        checkbutton_vars.append(var)
    
    checkbutton_vars_list.append(checkbutton_vars)
    button_delete = Button(frame, text="Delete", command=lambda i=index: delete_frame(frame,i))
    # button_delete.pack(side=RIGHT)
    button_delete.grid(row=5,column=3)

    frame_list.append(frame)

def toggle_selezione(*args):
    global opts_strvar, last_selected
    clicked_value = opts_strvar.get()
    
    if clicked_value == last_selected.get():
        opts_strvar.set('')  # Deseleziona il pulsante corrente
    else:
        last_selected.set(clicked_value)

def optsSelection(root):
    # Creazione dei Checkbutton
    global opts_var, opts_strvar, last_selected
    opts_list = list(analysis._dict_opts.keys())
    # opts_list = ["default","Diego","Matilde","Enzo","custom"]
    opts_strvar = StringVar()
    last_selected = StringVar(value="")  # Variabile di tracciamento per tenere traccia dell'ultimo pulsante selezionato
    for i in range(len(opts_list)):
        radiobutton = ttk.Radiobutton(root, text=opts_list[i], value=opts_list[i], variable=opts_strvar) #, command=lambda: show_selected(selection_label,index))
        # checkbutton.pack(anchor=W)
        radiobutton.grid(row=int(i/4),column=i)
    # Collega la funzione toggle_selezione alla variabile di tracciamento
    opts_strvar.trace_add("write", toggle_selezione)
    opts_var = opts_strvar.get()

def goAnalyze(export, vis_max, pdf_name):
    global frame_list, select_run_list, opts_strvar, opts_filter
    opts_filter_var = opts_filter.get()
    tmp = opts_filt_list.copy()
    tmp.remove("no filter")
    if opts_filter_var not in tmp:
        opts_filter_var = False

    keys = [run_id for run_id, var in zip(analysis.run_list.keys(),select_run_list) if var.get() != 0]
    cols = []
    if opts_strvar.get()!="":
        cols = opts_strvar.get()
    else:
        for index in range(len(frame_list)):
            cols.append(get_selected_values(index))
        if cols==[]:
            cols="default"
    if export.get()!=0:
        export = True
    if vis_max.get()!=0:
        vis_max = ["speed"]
    else:
        vis_max = []
    analysis.comparation(keys=keys,cols=cols,export_PDF=export,vis_max=vis_max,pdf_name=pdf_name.get(),filter=opts_filter_var)

def go(window,min_pick,min_dist):
    window.destroy()
    root = Tk()
    root.title("Insert data")
    root.geometry("520x340+700+150")   #dimensions of the window + positioning
    root.minsize(200,150)
    # root.maxsize(1200,900)
    root.iconbitmap("biking.ico")   #logo
    global frame_list, label_list, index_list, checkbutton_vars_list, select_run_list, opts_filter, calc_avgrun

    try:
        mp = float(min_pick)
    except ValueError:
        mp = False
    if not mp == False:
        min_pick = mp

    try:
        mp = float(min_dist)
    except ValueError:
        mp = False
    if not mp == False:
        min_dist = mp
    
    if calc_avgrun.get() == True:
        if min_pick == "":
            if min_dist == "":
                analysis.calcAvgRun(export=True)
            else:
                analysis.calcAvgRun(min_dist=min_dist, export=True)
        else:
            if min_dist == "":
                analysis.calcAvgRun(min_pick=min_pick, export=True)
            else:
                analysis.calcAvgRun(min_pick=min_pick,min_dist=min_dist, export=True)

    frame_list = []
    label_list = []
    index_list = ["timestamp","altitude","heart_rate","cadence","distance","speed","power","RPMw_bo_RPMp","ideal_speed","gear"]
    checkbutton_vars_list = []
    select_run_list = []
    # label_select_run = Label(root,text="Select one or more run")
    # label_select_run.pack(pady=5)
    frame_sel_run = LabelFrame(root,text="Select one or more run")
    frame_sel_run.pack(pady=5)
    selectRun(frame_sel_run)
    # lframe = LabelFrame(root, text="Graphs")
    # create_frame_with_button(lframe,frame_list,label_list)
    # Creazione del pulsante per aggiungere nuove coppie di Frame e Button
    add_button = Button(root, text="Add Plot", command=lambda: create_frame_with_button(root))
    add_button.pack(pady=5)
    
    chk_frame = Frame(root)
    chk_frame.pack(pady=5)
    exp = IntVar()
    export_button = Checkbutton(chk_frame, text="Export PDF", variable=exp)
    # export_button.pack(pady=5)
    export_button.grid(row=0,column=0)
    label = Label(chk_frame, text="pdf name: ")
    label.grid(row=1,column=0)
    pdf_name = StringVar()
    entry_pdf_name = ttk.Entry(chk_frame, width=50, textvariable=pdf_name)
    entry_pdf_name.grid(row=1,column=1)
    # entry_pdf_name.pack(pady=5) #, sticky=NSEW)

    vzmax = IntVar()
    vis_button = Checkbutton(chk_frame, text="visualize max (speed)", variable=vzmax)
    # export_button.pack(pady=5)
    vis_button.grid(row=0,column=1)
    
    opts_filter = StringVar()
    # last_selected = StringVar(value="")  # Variabile di tracciamento per tenere traccia dell'ultimo pulsante selezionato
    # opts_filt_list = ["rough","medium","extra","no filter"]
    for i in range(len(opts_filt_list)):
        radiobutton = ttk.Radiobutton(chk_frame, text=opts_filt_list[i], value=opts_filt_list[i], variable=opts_filter) #, command=lambda: show_selected(selection_label,index))
        # checkbutton.pack(anchor=W)
        radiobutton.grid(row=2,column=i)
    # Collega la funzione toggle_selezione alla variabile di tracciamento
    # opts_filter.trace_add("write", toggle_selezione)
    # TODO : controllo variabile inizializzata (valore selezionato)
    # opts_filter_var = opts_filter.get()
    # if opts_filter_var == "no filter":
    #     opts_filter_var = False
    
    go_button = Button(root, text="Let's go!", command=lambda: goAnalyze(exp,vzmax,pdf_name))#,opts_filter_var))
    go_button.pack(pady=5)
    
    frame_opts = LabelFrame(root,text="choose default plot scheme")
    frame_opts.pack(pady=5)
    optsSelection(frame_opts)
    
    root.mainloop()
    

# Create the main window
root = Tk()
root.title("Run Analysis")
root.geometry("1170x300+175+150")   #dimensions of the window + positioning
root.minsize(240,180)
root.maxsize(1200,900)
root.iconbitmap("biking.ico")   #logo

# Create the Analysis object
analysis = RunAnalysis()
entry_list = []
frame_list = []

# Create a Frame for file selection
frame1 = LabelFrame(root, text="Upload single run", background="skyblue")
frame_list.append(frame1)
# frame1.pack(padx=10, pady=10)
frame1.grid(row=0, column=1, padx=10, pady=10)
# frame1.place(relx=0.5,rely=0.1,anchor=CENTER)
file_path = generateEntry(frame1,"file",initialdir_file,0,entry_list)
cond_file_path = generateEntry(frame1,"settings file",initialdir_cond,1,entry_list)

frame2 = LabelFrame(root, text="Upload entire folder", background="orange")
frame_list.append(frame2)
# frame2.pack(padx=10, pady=10)
folder_path = generateEntry(frame2,"folder",initialdir_file,0,entry_list,folder=True)
cond_folder_path = generateEntry(frame2,"settings file",initialdir_cond,1,entry_list)

bt_single_run = Button(root,text="Upload single run",command=lambda: toggle_frame(0))
# bt_single_run.pack(padx=5,pady=5)
bt_single_run.grid(row=1, column=0, padx=5, pady=5)
# bt_single_run.place(relx=0.4,rely=0.6,anchor=CENTER)
bt_multiple_run = Button(root,text="Upload folder",command=lambda: toggle_frame(1))
# bt_multiple_run.pack(padx=5,pady=5)
bt_multiple_run.grid(row=1, column=2, padx=5, pady=5)
# bt_multiple_run.place(relx=0.6,rely=0.6,anchor=CENTER)


next_button = ttk.Button(root, text="Add run", command=lambda: nextRun(analysis,file_path,cond_file_path,folder_path,cond_folder_path,entry_list))
# next_button.pack(padx=5, pady=5)
next_button.grid(row=2, column=1, padx=5, pady=5)
# next_button.place(relx=0.4,rely=0.7,anchor=CENTER)

end_button = ttk.Button(root, text="Ok, let's go", command=lambda: go(root,min_pick.get(),min_dist.get()))
# end_button.pack(padx=5, pady=5)
end_button.grid(row=2, column=2, padx=5, pady=5)
# end_button.place(relx=0.6,rely=0.7,anchor=CENTER)

label = ttk.Label(root, text="min speed pick : ")
label.grid(row=3, column=0, padx=5, pady=5) #, sticky=NSEW)
min_pick = StringVar()
entry_file = ttk.Entry(root, width=50, textvariable=min_pick)
entry_file.grid(row=4, column=0, padx=5, pady=5) #, sticky=NSEW)

label = ttk.Label(root, text="min distance : ")
label.grid(row=3, column=2, padx=5, pady=5) #, sticky=NSEW)
min_dist = StringVar()
entry_file = ttk.Entry(root, width=50, textvariable=min_dist)
entry_file.grid(row=4, column=2, padx=5, pady=5) #, sticky=NSEW)

calc_avgrun = IntVar()
calc_avgrun_button = Checkbutton(root, text="Calculate Avg Run", variable=calc_avgrun)
calc_avgrun_button.grid(row=4,column=1)


root.mainloop()


