function[v]= simulazione(P, pendenzaNew, vento, cost,angolo,IdRun)

%global v T km data;

% Preparativi
[temp,umid,mbar,vel_vento,~,m,ruote,raggio,~] = readFile(IdRun);
coeff_file = 'coeff.csv'; 
coeff = csvread(coeff_file,0,0);        %leggo file coefficienti
N = 82;                                 %una riga per 100mt di gara
W = zeros(1,N);

% Assegnazione potenza (idea: potenza costante a tratti su intervalli di
% lunghezza multipla di 100 metri)
W(1:5) = P(1); % potenza nei primi 500 metri
W(6:15) = P(2);
W(16:30) = P(3);
W(31:50) = P(4);
W(51:70) = P(5);
W(71:82) = P(6); 

% Variabili
T = 400;                            % lunghezza aumentata del vettore per non avere problemi
v = zeros(1,T);                     % vettore delle velocità [m/s]
metri = zeros(1,T);                 % vettore delle distanze dal 1o rilevamento [m]
t = zeros(1,T);                     % vettore dei tempi [s]
cad = zeros(1,T);                   % vettore della cadenza [giri/min]

if(pendenzaNew)
    pendenza = readmatrix('pendenza_nuova_media_viagg.csv');
else
    pendenza = readmatrix('pendenza_migliorata.csv');
end

%% Da impostare: cond. ambientali e dati veicolo

I = 0.044;
Area = 0.28432;
PP=interpolazione_CD_CFD;
%PP=giov_PM_stoch.sfit;
RR=interpolazione_CR(ruote); 
rend = 0.97;

% Determino cond. atmos
Psat=6.1078*10^((7.5*(temp+273.15)-2048.625)/(temp+273.15-35.85));
rho=(mbar*100-umid*Psat)/(287.05*(temp+273.15))+(umid*Psat)/(461.495*(temp+273.15));
g = 9.81;


%% Inizializzo vettori/ matrici

% matrici di integrali
Ep=zeros(1,T-1);  
Ed=zeros(1,T-1);
Er=zeros(1,T-1);
y = zeros(1,T-1);
v_int=zeros(1,T-1);
v_int_con_vento = zeros(1,T-1); 
W_int= zeros(1,T-1);

% vettori di valori scalari
Ec=zeros(1,T); 
E_ruote=zeros(1,T);

v(1) = 18/3.6;

if (vento)
    if (cost)
        v_int_con_vento = zeros(T-1,1);    
        for jj = 1:T-1
            v_int_con_vento(jj) = 0.5*(v(jj)+v(jj+1)) + cos(angolo(1)/360*2*pi)*(vel_vento/3.6);
            Ed(jj) = 1/2*Area*rho*ppval(PP,v_int_con_vento(jj))*v_int_con_vento(jj)^2*v(jj+1);
        end
    else
        ang_i = angolo(1);% angolo vento rispetto alla strada nel punto di partenza
        ang_f = angolo(2);% angolo vento rispetto alla strada nel punto di arrivo
        f_vento = @(x) cos(x/360*2*pi)*(vel_vento/3.6); 
        f_var = (ang_i - ang_f)/(T-1); % variazione angolo in modo uniforme
        v_int_con_vento = zeros(T-1,1);
        for h = 1:T-1
            v_int_con_vento(h) = 0.5*(v(h)+v(h+1)) + f_vento(ang_i - (h-1)*f_var());
            Ed(h) = 1/2*Area*rho*ppval(PP,v_int_con_vento(h))*v_int_con_vento(h)^2*v(h+1);
        end
    end
   
end

for j = 1:1:T
           
            if j == 1
                      metri(1) = 1; 
                      metri(2) = round(v(1));
                      y(1)  =  sum(pendenza(metri(1):metri(2))); % somma mi da dislivello totale dell'intervallo
            else
                      j;
                      metri(j);
                      metri(j+1) = metri(j) + round(v(j));
                      y(j)  =  sum(pendenza(metri(j):metri(j+1)));
                      
            end
            
            % controllo se distanza massima raggiunta
            if metri(j) >= 8200
                n = j;
                break % ferma ciclo
            end
            
            Ep(j) =  m*g*y(j); % pendenza favorevole immette sempre energia
            
            % uso della formula del trapezio come formula di quadratura
            Ed(j) = 1/2*Area*rho*coeff(floor(v(j)*10),1)*v(j)^3;
            Er(j) =  m*g*coeff(floor(v(j)*10),2)*v(j);
            Ec(j) = 1/2*m*v(j)^2;   
            E_ruote(j)  = I*((v(j)/raggio)^2); % inerzia di due ruote
            
            ind = floor(metri(j)/100)+1;
            v(j+1) = sqrt((Ec(j)+E_ruote(j)+W(ind)*rend+Ep(j)-Er(j)-Ed(j))/(0.5*m+I/(raggio)^2));        
end

plot(metri(1:n),v(1:n),'*b')
grid on
xlabel('Distanza')
ylabel('Velocità')
end
