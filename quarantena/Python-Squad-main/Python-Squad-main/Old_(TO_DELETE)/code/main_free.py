'''
Please run THIS file INSTEAD OF "main.py"
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
import os
os.chdir(os.path.dirname(__file__))    #path della cartella che contiene il progetto


## do not delete ##  useful/necessary variables
#########################################################
dataset_path_Matilde = util.getDatasetPath("Matilde")
dataset_path_Diego = util.getDatasetPath("Diego")
dataset_path_Enzo = util.getDatasetPath("Enzo")

dtsettings_file_Matilde = util.getSettingsPath("Matilde")
dtsettings_file_Diego = util.getSettingsPath("Diego")
dtsettings_file_Enzo = util.getSettingsPath("Enzo")

an_run_Matilde = RunAnalysis()
an_run_Enzo = RunAnalysis()
an_run_Diego = RunAnalysis()
#########################################################


## EXAMPLE
# upload an entire folder (Diego)
an_run_Diego.uploadFolder(folder_path=dataset_path_Diego, settings_file=dtsettings_file_Diego)

# upload a single run
# file_name = util.joinPath(dataset_path_Diego, "Diego_15_09_2023_AM_2.csv")
# an_run_Diego.addSettings(settings_file=dtsettings_file_Diego)
# an_run_Diego.addRun(file_name=file_name)


# comparate some races
an_run_Diego.comparation(keys=["Diego_15_09_2023_PM_2","Diego_16_09_2023_AM_2"], cols="Diego", export_PDF=True,export_PNG=True, show=True, vis_max=["speed","power"])

an_run_Diego.rmRun("Diego_12_09_2023_AM")
an_run_Diego.calcAvgRun()

# plot the average run
an_run_Diego.run_list["avg_run"].plot(export=True)
# an_run_Diego.run_list["avg_run"].calcDisplacement()
# print("disp:  "+str(an_run_Diego.run_list["avg_run"].disp))

