function PP=interpolazione_CD_CFD

% dovrebbero essere i valori della simulazione CFD
% il quadro generale: loro fanno la simulazione CFD

V = [30:10:100 105:5:150]/3.6;

% valori di Taurus
Cd = [0.04047 0.03601 0.03308 0.03102 0.02973 0.03069 0.03548 0.03758 ...
                  0.03778 0.03792 0.03817 0.03852 0.03901 0.03986 0.04076 ...
                  0.04097 0.04120 0.04124];

fitv=0:0.1:45;
figure
plot(V,Cd,V,Cd) % '*',fitv,ppval(PP_ph,fitv),V,Cd_ph,'x'
legend('Cd Taurus') % ,'Cd Phoenix'
grid on


PP=pchip(V,Cd);
