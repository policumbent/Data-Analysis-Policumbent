from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from run import *
import os
os.chdir(os.path.dirname(__file__))

# # Utilizzare dir() per ottenere la lista degli attributi
# attributes = dir(example_obj)

# # Filtrare gli attributi che non iniziano con '__' (attributi speciali)
# attribute_names = [attribute for attribute in attributes if not attribute.startswith('__')]

check_next = False

def closew1():
    closeWindow(window1)
    
def closeWindow(window):
    global check_next
    check_next = True
    window.destroy()

def go():
    global run, vhc, dr, wl, gb
    run = Run()
    vhc = Vehicle()
    dr = Driver()
    wl = Wheel()
    gb = GearBox()
    ######################################################################
    # inserire valori negli oggetti
    # conversione della gear box in lista tramite separatore ',' o ' '
    ######################################################################
    run.readRun(file_path)
    bk = BikeInfo(vhc,dr,wl,gb)
    run.setBikeInfo(bk)
    run.gearChangeDetect()
    closeWindow(root)
    
def startAnalysis():
    closeWindow(window2)
    global arun
    arun = RunAnalysis()
    arun.addRun(run)
    arun.plotEach()

def select_file():
    file_path = filedialog.askopenfilename()
    entry_file.delete(0, END)  # Clear the Entry before inserting the new path
    entry_file.insert(0, file_path)  # Insert the new path into the Entry

# Create the first window
window1 = Tk()
window1.title("Choose")
window1.geometry("200x150+655+200")   #dimensions of the window
window1.minsize(100,75)
window1.maxsize(800,600)
window1.iconbitmap("biking.ico")   #logo

attributes = StringVar()
radio1 = Radiobutton(window1, text="All", value="a", variable=attributes)
radio2 = Radiobutton(window1, text="Only necessary", value="n", variable=attributes)
radio3 = Radiobutton(window1, text="Only necessary and names", value="nn", variable=attributes)
radio1.pack()
radio2.pack()
radio3.pack()
button = Button(window1, text="Next", command=closew1)
button.pack()

window1.mainloop()

if check_next == True:
    check_next = False
    # Create the main window
    root = Tk()
    root.title("Insert data")
    root.geometry("900x400+310+120")   #dimensions of the window
    root.minsize(240,180)
    root.maxsize(1200,900)
    root.iconbitmap("biking.ico")   #logo

    # Create a Frame for file selection
    frame1 = Frame(root, background="yellow")
    frame1.pack(padx=10, pady=10)
    label = Label(frame1, text="file path:")
    label.grid(row=0, column=0, padx=5, pady=5) #, sticky=NSEW)

    # Get the file path
    file_path = StringVar()
    entry_file = ttk.Entry(frame1, width=50, textvariable=file_path)
    entry_file.grid(row=0, column=1, padx=5, pady=5) #, sticky=NSEW)

    # Create a button to select a file
    select_button = Button(frame1, text="Select a File", command=select_file)
    select_button.grid(row=0, column=2, padx=5, pady=5) #, sticky=NSEW)

    frame_1234 = LabelFrame(root, text="Bike Info")
    frame_1234.pack(fill=X, pady=10)

    frame2 = LabelFrame(frame_1234, text="Vehicle", background="#00FFFF")   #"#F0F8FF")
    frame2.pack(side=LEFT,fill=BOTH, pady=10, expand=True)

    vehicle_compulsary = []
    vehicle_semicomp = ["name"]
    vehicle = ["name", "chassis_weight", "hull_weight", "frontal_area", "inertia", "leg_traction", "crank"]
    if attributes.get() == "n":
        vehicle = vehicle_compulsary
    elif attributes.get() == "nn":
        vehicle = vehicle_semicomp
    if vehicle == []:
        label = Label(frame2, text="No necessary data")
        label.pack(padx=5, pady=5)
    else:
        vhc_vars = []
        for i, value in enumerate(vehicle):
            label = Label(frame2, text=f"{vehicle[i]}:")
            label.grid(row=i, column=0, padx=5, pady=5) #, sticky=NSEW)

            vhc_vars.append(StringVar())
            entry_value = Entry(frame2, width=20, textvariable=vhc_vars[i])
            entry_value.grid(row=i, column=1, padx=5, pady=5)

    frame3 = LabelFrame(frame_1234, text="Driver", background="#8A2BE2")
    frame3.pack(side=LEFT, fill=BOTH, pady=10, expand=True)

    driver_compulsary = []
    driver_semicomp = ["name"]
    driver = ["name", "weight"]
    if attributes.get() == "n":
        driver = driver_compulsary
    elif attributes.get() == "nn":
        driver = driver_semicomp
    if driver == []:
        label = Label(frame3, text="No necessary data")
        label.pack(padx=5, pady=5)
    else:
        drv_vars = []
        for i, value in enumerate(driver):
            label = Label(frame3, text=f"{driver[i]}:")
            label.grid(row=i, column=0, padx=5, pady=5) #, sticky=NSEW)

            drv_vars.append(StringVar())
            entry_value = Entry(frame3, width=20, textvariable=drv_vars[i])
            entry_value.grid(row=i, column=1, padx=5, pady=5)

    frame4 = LabelFrame(frame_1234, text="Wheels", background="#7FFFD4")
    frame4.pack(side=LEFT, fill=BOTH, pady=10, expand=True)

    wheels_compulsary = ["radius"]
    wheels_semicomp = ["tyre", "radius"]
    wheels = ["tyre", "pressure", "radius", "rolling_circum", "inertia"]
    if attributes.get() == "n":
        wheels = wheels_compulsary
    elif attributes.get() == "nn":
        wheels = wheels_semicomp
    if wheels == []:
        label = Label(frame4, text="No necessary data")
        label.pack(padx=5, pady=5)
    else:
        wls_vars = []
        for i, value in enumerate(wheels):
            label = Label(frame4, text=f"{wheels[i]}:")
            label.grid(row=i, column=0, padx=5, pady=5) #, sticky=NSEW)

            wls_vars.append(StringVar())
            entry_value = Entry(frame4, width=20, textvariable=wls_vars[i])
            entry_value.grid(row=i, column=1, padx=5, pady=5)

    frame5 = LabelFrame(frame_1234, text="Gear Box", background="#FF7F50")
    frame5.pack(side=LEFT, fill=BOTH, pady=10, expand=True)

    gear_compulsary = ["gear_box", "chainring", "sec_ratio"]
    gear_semicomp = ["gear_box", "chainring", "sec_ratio"]
    gear = ["gear_box", "chainring", "sec_ratio"]
    if attributes.get() == "n":
        gear = gear_compulsary
    elif attributes.get() == "nn":
        gear = gear_semicomp
    if gear == []:
        label = Label(frame5, text="No necessary data")
        label.pack(padx=5, pady=5)
    else:
        gr_vars = []
        for i, value in enumerate(gear):
            label = Label(frame5, text=f"{gear[i]}:")
            label.grid(row=i, column=0, padx=5, pady=5) #, sticky=NSEW)

            gr_vars.append(StringVar())
            entry_value = Entry(frame5, width=20, textvariable=gr_vars[i])
            entry_value.grid(row=i, column=1, padx=5, pady=5)

    button = Button(root, text="Go!", command=go)
    button.pack()   #(side=BOTTOM, padx=5, pady=5)
    root.mainloop()
    
if check_next == True:
    check_next = False
    window2 = Tk()
    label = Label(window2, text="Let's start the analysis!")
    label.pack(padx=5, pady=5)
    entry_value1 = Button(window2, text="Yes", command=startAnalysis)
    entry_value2 = Button(window2, text="No", command=lambda: window2.destroy)
    entry_value1.pack(padx=5, pady=5)
    entry_value2.pack(padx=5, pady=5)
    window2.mainloop()