'''
TO READ:

If you want to try/use this code
please run "main_free.py" INSTEAD OF "main.py"
Just for safety :)
'''


'''
Date: 15/11/2023
cosa fa questo codice?
prende i dati delle run (che sono salvati in dei file csv) e li rielabora per produrre dei valori
e dei grafici significativi e utili per l'analisi della run.
È un codice abbastanza versatile, e permette di avere molta flessibilità sugli output che si vogliono
visualizzare.
Per un oggetto RunAnalysis si possono selezionare manualmente i dati che si intende visualizzare,
già divisi per plot (ad esempio, si possono rappresentare i profili di "power" e "speed" in una finestra,
mentre la "speed" e la "ideal_speed" in un'altra).
Si possono anche selezionare delle opzioni (opts) preimpostate, che corrispondono a dei blocchi di grafici
predefiniti, associati alle preferenze usuali dei ciclisti e/o di chi analizzerà i dati.
C'è anche un modulo di simulazione, ma è ancora da sistemare.
Però nel frattempo tu...
crea una copia di questo codice nel tuo PC e divertiti a cambiare i parametri a tuo piacimento!

N.B. i path utilizzati in questo codice sono path relativi. Ricordati di non spostare i file, altrimenti
nulla funzionerà più :)
'''
from run import *
import util
import numpy as np
import os
os.chdir(os.path.dirname(__file__))    #path della cartella che contiene il progetto
#print(os.getcwd())



## main di prova ##

dataset_path_Matilde = util.getDatasetPath("Matilde")
dataset_path_Diego = util.getDatasetPath("Diego")
dataset_path_Enzo = util.getDatasetPath("Enzo")

dtsettings_file_Matilde = util.getSettingsPath("Matilde")
dtsettings_file_Diego = util.getSettingsPath("Diego")
dtsettings_file_Enzo = util.getSettingsPath("Enzo")

plot_opts_file = util.getPlotOptsPath()

an_run_Matilde = RunAnalysis()
an_run_Enzo = RunAnalysis()
an_run_Diego = RunAnalysis()

# "BM_130923_AM1.csv"

# ## upload an entire folder (Matilde)
# # conditions_path = util.getCondPath("Phoenix_Matilde.xlsx")
# an_run_Matilde.uploadFolder(folder_path=dataset_path_Matilde, settings_file=dtsettings_file_Matilde)

# an_run_Matilde.comparation(cols="Matilde", export_PDF=False, show=True, vis_max=["speed"])   #comparation between specified or default run with complete arbitrariness on the management of graphs

# ## upload an entire folder (Enzo)
# # conditions_path = util.getCondPath("Phoenix_Enzo.xlsx")
# an_run_Enzo.uploadFolder(folder_path=dataset_path_Enzo, settings_file=dtsettings_file_Enzo)

# an_run_Enzo.comparation(cols="Enzo", export_PDF=False, show=True, vis_max=["speed"])

## upload an entire folder (Diego)
# conditions_path = util.getCondPath("Cerberus_Diego.xlsx")
an_run_Diego.uploadFolder(folder_path=dataset_path_Diego, settings_file=dtsettings_file_Diego, replace=False)

# comparate some races (Diego)
# an_run_Diego.plotEach()
#an_run_Diego.comparation(cols="Diego", export_PDF=True, show=True, vis_max=["speed"])
# an_run_Diego.calcAvgRun2()
an_run_Diego.rmRun("Diego_12_09_2023_AM") #è una run troppo corta
an_run_Diego.calcAvgRun(min_pick=60, min_dist=0, export=True)
an_run_Diego.comparation(cols="Diego", export_PDF=True, show=True, export_PNG=False,filter="rough",pdf_name="prova_filtro_rough") #, vis_max=["speed"])
# an_run_Diego.comparation(keys=["Diego_15_09_2023_AM_2","avg_run"],cols="Diego", export_PDF=False, show=True, export_PNG=True) #, vis_max=["speed"])

#["Diego_15_09_2023_AM_2"]

#___________________
# # upload a single run
# file_name = util.joinPath(dataset_path_Diego, "Diego_15_09_2023_AM_2.csv")
# cond_file = util.getCondPath("Cerberus_Diego.xlsx")
# # {
# run = Run(file_name=file_name, cond_file=cond_file)
# #or, better
# # run = Run(file_name=file_name,settings_file=dtsettings_file_Diego)
# an_run_Diego.addRun(run=run)
# # }
# #or, better and better, just
# # an_run_Diego.addSettings(settings_file=dtsettings_file_Diego)
# # an_run_Diego.addRun(file_name=file_name)


# The following examples could be wrong or inaccurate

#####################################
#TODO : correggere gli esempi
#####################################

## example of uploading a single run (Matilde)
# run1 = Run()
# file_name = util.joinPath(dataset_path_Matilde, "Matilde_15_09_2023_AM.csv")
# run1.bike_info.getInfoFromExcel(util.getCondPath("Phoenix_Matilde.xlsx"))
# run1.readRun(file_name)
# run1.plot(cols=["speed","altitude"])
# an_run_Matilde.addRun(run1)

## example of uploading two run singly (Diego)
# run2 = Run()
# file_name = util.joinPath(dataset_path_Diego, "Diego_15_09_2023_AM_2.csv")
# run2.bike_info.getInfoFromExcel(util.getCondPath("Cerberus_Diego.xlsx"))
# run2.readRun(file_name)
# run2.gearChangeDetect(initial_gear=1)
# an_run_Diego.addRun(run2)

# run3 = Run()
# file_name = util.joinPath(dataset_path_Diego, "Diego_13_09_2023_AM_2.csv")
# run3.bike_info.getInfoFromCsv(util.getCondPath("Cerberus_Diego.csv"))
# run3.readRun(file_name)
# run2.gearChangeDetect(initial_gear=1)
# an_run_Diego.addRun(run3)

#___________________
## Run object : manual initialization
#
# # for Matilde
# gb1 = GearBox(gear_box=[40,35,31,27,24,21,19,17,15,14,13,12], chainring=108, sec_ratio=[38,18])
# wl1 = Wheels(tyre="Michelin-blue", radius=0.23157)
# bk1 = BikeInfo(Vehicle("Phoenix"), Driver("Matilde"), wl1, gb1)
# run1.setBikeInfo(bk1)
# # for Diego:
# gb3 = GearBox(gear_box=[32,28,24,21,19,17,15], chainring=60, sec_ratio=[54,17])
# wl3 = Wheels("Michelin-blue",None,0.23157,None,None)
# bk3 = BikeInfo(Vehicle("Cerberus"),Driver("Diego"),wl3,gb3)
# run3.setBikeInfo(bk3)

#___________________
## other stuff we can do with a Run object
#
# run2.setBounds(lwbd=3,upbd=3)  #cut 3 lines from the beginning and the end of the dataset
# run2.gearChangeDetect()
# run2.exportCols("prova.csv", ['gear', 'speed'])   #export a csv file with selected cols
# run2.plot(cols=["speed","ideal_speed"])
# run2.export()   #export a PDF file with the principal graphs
# print(run2.disp)   #displacement

#___________________
## RunAnalysis object
#
# an_run_Diego.plotEach(export=True)   #plot and export each run, representing specified or default cols
# an_run_Diego.comparation(keys=["Diego_15_09_2023_AM_2.csv","Diego_13_09_2023_AM_2.csv"],
#                    cols=[["speed","heart_rate"],["power", "heart_rate"],["ideal_speed","power","altitude"]],export_PDF=True)   #complete arbitrariness on the management of graphs
# an_run_Diego.calcAvgRun()
# an_run_Diego.run_list["avg_run"].plot()   #plot the average run

# model and simulation
# an_run_Diego.modeling(degree=3, input_values=["power","heart_rate","cadence"],output_value="speed",plot=True)   #create the model based on power, heart rate and cadence
# an_run_Diego.simulate(plot=True)














'''
# do not consider

# print(run1.run_data.iloc[0:7][['speed','gear','RPMw_bo_RPMp','ideal_speed']])
# print(run1.run_data[['speed','gear','cadence','RPMw_bo_RPMp','ideal_speed']])

# print(run2.bike_info.bike.chassis_weight)
# print(math.isnan(run2.bike_info.bike.chassis_weight))

# print(run3.bike_info.bike.chassis_weight)
# print(math.isnan(run3.bike_info.bike.chassis_weight))
'''
