## Comandi utili da cmd (linea di comando):

$ lm    #lista variabili
$ ls    #lista file nella cartella corrente
$ cd    #change directory, modifica la cartella corrente
#es.
$ cd nome_cartella   #si sposta nella cartella indicata
$ cd ..   #si sposta nella cartella precedente
$ cd dir1/dir2/dir3   #si può concatenare un intero percorso con il simbolo "/"
$ vim [nome_file.estensione]    #crea un file
{ esc  :x  (oppure) :wq }    #comandi per chiudere il file generato
w = write (save), q = quit, x = exit

$ cat [nome_file.estensione]    #visualizza il contenuto di un file (in realtà sta per "concatenate")
$ mkdir [nome_nuova_cartella]    #make directory, crea una nuova cartella nella cartella corrente
_____________________________________________________________________
## Git:
#installa Git: https://git-scm.com/downloads
#verifica che premendo tasto dx sullo schermo compaia la voce "Git bash" (cerca anche in "altre opzioni")

#tutti i comandi che iniziano con $ puoi eseguirli nella Power Shell oppure nel terminale che offre Git (Git bash)

#crea un profilo GitHub: https://github.com
_____________________________________________________________________
## Generare una chiave (non obbligatorio):

#crea chiave SSH:
$ ssh-keygen -t ed25519 -C "your_email@example.com"
aggiungi password ...

#aggiungi la chiave al tuo profilo:
$ ssh-add ~/.ssh/id_ed25519

#aggiungi la chiave al profilo GitHub:
$ clip < ~/.ssh/id_ed25519.pub   #copia la chiave
#apri GitHub, sezione "settings -> SSH & GPG keys -> new SSH key"
#incolla la chiave nella sezione "key"; in "title" puoi mettere "personal laptop" e lasciare "Authentication key"
_____________________________________________________________________
## Creare una cartella condivisa:
#si crea una repository in GitHub, dopodiché si crea una copia locale

#apri GitHub, impostazioni in alto a dx, sezione "repository -> new"; (licenza consigliata per studenti : MIT License)
#copia la chiave SSH (o HTTPS):
#seleziona la repository, vai su "code -> local -> SSH" e copia la chiave (se non hai una chiave utilizza il codice https)
#crea una copia locale della repository sul tuo pc:
$ git clone [chiave SSH]   (o https)
#ora puoi creare in questa cartella dei nuovi file (come faresti normalmente)
N.B. tutto ciò che fai in questa cartella è in locale, quindi NON risulterà nulla nella repository GitHub

## Modifica della directory GitHub:

#si aggiungono/modificano/rimuovono file nella cartella locale, poi si comunicano le modifiche alla directory GitHub:
#per aggiungere le modifiche a GitHub bisogna prima aggiungerle a Git, e poi "pusharle" nella repository:
#aggiungi i file a Git:
$ git add [nome file completo con estensione]   #va fatto per ogni file; puoi anche usare l'opzione -a (all) per aggiungerli tutti (quindi "$ git add -a" o anche "$ git add .")
$ git commit -m "commento"   #il commento può anche essere semplicemente il numero della versione
#aggiorna la repository GitHub:
$ git push   #va eseguito nella directory collegata a GitHub

#se qualcun altro ha modificato la repository GitHub condivisa:
#aggiorna la copia locale della repository:
$ git pull   #va eseguito nella directory collegata a GitHub
_____________________________________________________________________
## Creare la cartella in locale e poi aggiungerla a GitHub:

## crea cartella per Git (personale, per usufruire dei servizi* di Git):
crea una cartella (nella directory che vuoi):
$ mkdir MyFolder   #puoi anche crearla banalmente con il classico tasto dx -> nuovo -> cartella
#collega la cartella a Git:
$ git init   #va eseguito nella directory che si intende aggiungere a GitHub
#comparirà una cartella .git (se non compare vai su "visualizza -> mostra -> elementi nascosti")
#crea i file che vuoi come in una cartella normale
$ git add [nome file completo con estensione]   #come sopra
$ git commit -m "commento"   #come sopra

## aggiungi a GitHub:  (per aggiungere a GitHub una cartella esistente in locale)

git remote add origin git@github.com:G48R1/Progetto_PCS.git    # nome_Git_Hub/nome_progetto.git
git branch -M main   #crea il branch master
git push -u origin main   #carica il branch generato
_____________________________________________________________________
## BRANCHING & MERGING
#lavoro in parallelo: creare diramazioni del tronco principale (master) e poi riconnetterle al master:

$ git branch   #restituisce la lista dei branches
#creare un branch:
$ git branch [nome_branch]   #crea un branch
#spostarsi da un branch a un altro:
$ git checkout [nome_branch]   #per tornare sul principale si usa git checkout master
$ git checkout -b [nome_branch]    #creare un nuovo branch e switchare dentro direttamente

$ git config --global user.email "email@"   #configura l'autore

#comunicare alla repository GitHub che ho creato un nuovo branch:
#update della repository GitHub   (da fare nel branch che si vuole diramare)
$ git push --set-upstream origin [nome_branch]
$ git push origin [nome_branch]
#qual è la differenza tra "origin" e "--set-upstream origin"?
#è complicato, ma in sostanza è meglio usare "--set-upstream origin" (OSS. puoi abbreviare "--set-upstream" in "-u", dunque "$ git push -u origin [nome_branch]")

################# oppure direttamente merging: (se non si vuole creare il branch anche su GitHub ma solo in locale)
## riconnessione al master:
#il merge integra i contenuti del branch in cui ci si trova con quelli del branch indicato
$ git checkout master   #mi sposto nel master
$ git merge [nome_branch]   #copio le novità di nome_branch in master
$ git push   //per aggiornare la repository GitHub
#OSS. posso anche fare un merge del master su un branch secondario, con la stessa procedura

#struttura del merging e problemi (contrasti):
#quando si vuole fare un merge nel master conviene prima assicurarsi che non ci siano conflitti con eventuali merge realizzati da altri utenti.
#quindi ci si riallinea prima al master, e poi si fa il merge:
$ git checkout [nome_branch]
$ git merge master      (mi riallineo all'ultima versione del master, facendo il merge nel mio ramo. In questo modo evito i conflitti con i merge fatti da altri utenti da altri branch)
#in questa fase possono sorgere conflitti:
//volendo: $ git mergetool (per visualizzazione grafica)
#modifico il file che crea il conflitto (lo apro e modifico le righe evidenziate), poi lo riaggiungo a Git e aggiorno GitHub:
git add [nome_file]
git commit -m "commento"
git push
#il merge proseguirà da solo
#risolta questa fase si può proseguire con il merge vero e proprio del branch nel master (stesso procedimento)


$ git branch -d [nome_branch]     (elimina branch)  N.B. di solito non si fa, a meno che non serva spazio
$ git branch -r    (lista dei branch in remoto, quindi da GitHub)
_____________________________________________________________________
## Altri comandi:

$ git config [...]  #es. user.name, user.email
$ git config user.name "Mario"
$ git config --list   #lista delle info dell'utente
$ git config --global init.defaultBranch main  #cambiare nome al master (così si chiama main)

$ git diff {--staged}   (mostra le differenze tra il file modificato e l'ultimo commit)

$ git restore [nome_file.estensione]    #ripristina file cancellato/modificato
$ git restore --staged [nome_file.estensione]    #è un ctrl+z di add

$ git status    #stampa le info sullo stato del file [modifiche/aggiornamenti]
$ git status -s (o --short) #versione breve dell'output
$ git commit {--amend} -m "[es. add: new version]"    #aggiorna e aggiunge un commento alla versione modificata; amend permette di rieffettuare la commit e sovrascrivere il messaggio; per lasciare il messaggio inalterato usare [git commit --amend --no-edit]

$ git log    #storico delle versioni (commit)
$ git log --since=2.weeks   #es. "2008-01-15" oppure "2 years 1 day 3 minutes ago"   #storico delle commit a partire dal tempo indicato

$ git tag  (-l o --list opzionali)    #lista dei tag delle versioni precedenti (codici delle commit)
$ git show [tag]    #mostra info sul tag inserito
$ git checkout [tag]    #sposta la repository alla versione indicata del progetto


_____________________________________________________________________
## PROBLEMI & ERRORI

$ ssh -T git@github.com    #impossibilità di effettuare una push (probabile errore di autenticazione)

DOCUMENTAZIONE
https://help.github.com/articles/testing-your-ssh-connection/
https://help.github.com/articles/connecting-to-github-with-ssh/


*La principale funzionalità di Git è la possibilità di accedere alle versioni precedenti della repository, poiché Git salva tutto lo storico delle modifiche
