function [vel] = velocitaSimulata(pendenza, vento, cost,IdRun,angolo)

coeff = raff_stima_coeff_nuovo(pendenza, vento,cost, IdRun);
P = analisi_run(IdRun);
v = simulazione(P, pendenza, vento, cost, angolo,IdRun);

ind = find(v < 1);
vel = v(ind - 1) * 3.6;

end
