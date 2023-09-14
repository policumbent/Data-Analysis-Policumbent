function PP_ph=interpolazione_CD_CFD

V = [30:10:100 105:5:150]/3.6;

% valori di Taurus
Cd = [0.04047 0.03601 0.03308 0.03102 0.02973 0.03069 0.03548 0.03758 ...
                  0.03778 0.03792 0.03817 0.03852 0.03901 0.03986 0.04076 ...
                  0.04097 0.04120 0.04124];

PP=pchip(V,Cd);

% Valori Phoenix

Cd_ph = [0.04179 0.03765 0.03503 0.03315 0.03172 0.03058 0.02981 0.02972 0.02972 ...
    0.02981 0.03010 0.03061 0.03133 0.03255 0.03397 0.03517 0.03648 0.03770];

PP_ph=pchip(V,Cd_ph);

fitv=0:0.1:45;
figure('NumberTitle', 'off', 'Name', 'Grafico di interpolazione Cd')
plot(fitv,ppval(PP,fitv),V,Cd,'*',fitv,ppval(PP_ph,fitv),V,Cd_ph,'x')
legend('Cd Taurus','Dati', 'Cd Phoenix','Dati')
grid on
end
