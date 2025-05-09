function RR=interpolazione_CR(ruote)

% v_banco = [15 30 45 55 70 90 105 120 130 140 150]/3.6;

% alternativa
v_banco = [0 30 45 55 70 90 105 120 130 140 150]/3.6;

if strcmp(string(ruote),'Continental')==1
% Conti 26 LTD
% cr_banco = [0.0038 0.0037 0.0041 0.0043 0.0048 0.0053 0.0056 0.0059 0.0061 0.0063 0.0064];

% alternativa
 cr_banco = [0.0034 0.0037 0.0041 0.0043 0.0048 0.0053 0.0056 0.0059 0.0061 0.0063 0.0064];

else
% Michelin 20'
%cr_banco = [0.0030 0.0030 0.0032 0.0033 0.0035 0.0037 0.0038 0.0040 0.0040 0.0041 0.0041];

% alternativa
 cr_banco = [0.0027 0.0030 0.0032 0.0033 0.0035 0.0037 0.0038 0.0040 0.0040 0.0041 0.0041];        
end

RR = pchip(v_banco,cr_banco);

% fitv=0:0.1:45;
% figure
% plot(fitv,ppval(RR,fitv),v_banco,cr_banco,'*')
% grid on
end

