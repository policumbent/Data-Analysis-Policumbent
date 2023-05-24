
clc
clear all
close all

data = csvread('2019_11_30_balocco_sessione_2.csv',1,0);
% fine = length(data(1:end,1));
fine = 626;
inizio = 464; % nuova lunghezza del csv
corr = 0.9897;

% cambiare riga di fine lettura, eventualmente applicare fattore correttuvo
for i=inizio:fine
        distanza_nuovo(i-inizio+1) = (data(i,5)-data(inizio,5))*corr;
end

% correzione raggio della ruota; fattore è sempre da determinare
for i=inizio:fine
         v_nuovo(i-inizio+1)  = data(i,3)*corr;
end

data_nuovo = [data(inizio:fine,1) data(inizio:fine,2) v_nuovo' data(inizio:fine,4) distanza_nuovo' ...
                  data(inizio:fine,6) data(inizio:fine,7) data(inizio:fine,8) data(inizio:fine,9)];

csvwrite('2019_11_30_balocco_sessione_2_rip_1.csv',data_nuovo);

