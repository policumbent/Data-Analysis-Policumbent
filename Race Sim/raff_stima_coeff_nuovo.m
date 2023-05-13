
function [nome_scrittura] = raff_stima_coeff_nuovo(pendanzaNew, vento,cost, IdRun)

global v T km data;

[temp,umid,mbar,vel_vento,angolo,m,ruote,raggio,IdRun] = readFile(IdRun);

data=csvread(IdRun,1,0);        %leggo csv della prova (aggiungere 1,0 se necessario)
T=length(data(:,1));            %qtà di rilevazioni [adim]
v=data(:,3)/3.6;                %vettore delle velocità [m/s]
metri=data(:,5)*10^3;           %vettore delle distanze dal 1o rilevamento [m]
W = data(:,4);

if (pendanzaNew)
    pendenza = csvread('pendenza_nuova_media_viagg.csv',0,0);
else
    pendenza = csvread('pendenza_migliorata.csv',0,0);
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
W_int= zeros(1,T-1);

% vettori di valori scalari
Ec=zeros(1,T); 
E_ruote=zeros(1,T);
A = zeros(T,1);
B = zeros(T,1); 

%% Pulisco dati correggendo grandi errori di misurazione salti maggiori di 3 km/h
for j = 2:T-2
    if v(j)>(v(j-1) + 3/3.6)
           v(j) = 0.5*(v(j-1)+v(j+1));
    end
end
%% Determino integrali sugli intervalli/ potenza

% j indice sull'intervallo <-> invece indice i per l'i-esimo valore registrato in tempo
for j =1:T-1
            if j == 1
                      m1 = 1;
                      m2 = round(metri(2));
            else
                      m1 = round(metri(j));
                      m2 = round(metri(j+1));   
            end
            
             v_int(j) = 0.5*(v(j)+v(j+1));
            
            % Determino velocità sull'intervallo
            if j > 2 && j < T-1
                W_int(j) = 1/3*(W(j-1)+W(j)+W(j+1));
            else
                W_int(j) = 0.5*(W(j)+W(j+1));
            end
            
            y(j) =  sum(pendenza(m1:m2)); % somma mi da dislivello totale dell'intervallo
            Ep(j) =  m*g*y(j); % pendenza favorevole immette sempre energia
            
            % uso della formula del trapezio come formula di quadratura
            Ed(j) = 1/2*Area*rho*ppval(PP,v_int(j))*v_int(j)^2*v(j+1);
            Er(j) =  m*g*ppval(RR,v_int(j))*v(j+1);
    
end

%%  Determino valori scalari
for i = 1:T
            Ec(i) = 1/2*m*v(i)^2;   
            E_ruote(i)  = I*(v(i)/raggio)^2;       
end

%% Vento
if (vento)
    if (cost)
        v_int_con_vento = zeros(T-1,1);    
        for j = 1:T-1
            v_int_con_vento(j) = 0.5*(v(j)+v(j+1)) + cos(angolo(1)/360*2*pi)*(vel_vento/3.6);
            Ed(j) = 1/2*Area*rho*ppval(PP,v_int_con_vento(j))*v_int_con_vento(j)^2*v(j+1);
        end
    else
        ang_i = angolo(1);% angolo vento rispetto alla strada nel punto di partenza
        ang_f = angolo(2);% angolo vento rispetto alla strada nel punto di arrivo
        f_vento = @(x) cos(x/360*2*pi)*(vel_vento/3.6); 
        f_var = (ang_i - ang_f)/(T-1); % variazione angolo in modo uniforme
        v_int_con_vento = zeros(T-1,1);
        for j = 1:T-1
            v_int_con_vento(j) = 0.5*(v(j)+v(j+1)) + f_vento(ang_i - (j-1)*f_var());
            Ed(j) = 1/2*Area*rho*ppval(PP,v_int_con_vento(j))*v_int_con_vento(j)^2*v(j+1);
        end
    end
   
end

%% Determino A,B e stima
A = [Ed' Er'];
B = zeros(T-1,1);
for j=1:T-1
          B(j) = Ec(j) - Ec(j+1) + E_ruote(j)-E_ruote(j+1) + Ep(j) + W_int(j)*rend; %  
end

% Impostazione intervallo di fine/ inizio alternativi
int_fine = T-1;
% int_fine = 283; % per giov PM
int_inizio = find(v>10);
int_inizio = int_inizio(1);
% int_fine = find(v>(120/3.6));
% int_fine = int_fine(1);

c = A(int_inizio:int_fine,:)\B(int_inizio:int_fine); % Ax = b dove x_1 = coeff_corr_cd , x_2 

Ed_corr = Ed*c(1);
Er_corr = Er*c(2);

ordine_scarto = zeros(1,T-1);
scarto=zeros(1,T-1);
for j=1:T-1         
        scarto(j)= Ec(j) - Ec(j+1) + E_ruote(j)-E_ruote(j+1) + Ep(j) + W_int(j)*rend...
            - Er_corr(j) - Ed_corr(j);
        ordine_scarto(j) = scarto(j)/Ec(j+1); 
end
    


%% ciclo per determinare Cd sperimentale
B = zeros(T-1,1);
denom = zeros(1,T-1);
Ed_stoch = zeros(1,T-1);
c_prod = 1;

    
    % Lancio cdspe ed aggiorno l'energia dissipata per drag
    lung = 10;
    
    if (vento)
        for j=1:T-1
            denom(j) = (1/2*rho*Area*v_int_con_vento(j)^2*v(j+1));
        end
        [ordine_scarto,ordine_scarto_vecchio,Cd_spe_reg] = cdspe(scarto,ordine_scarto,Ec,Ed_corr,denom);
        for j = 1:T-1
            Ed_stoch(j) = 1/2*Area*rho*ppval(PP,v_int(j))*v_int_con_vento(j)^2*v(j+1);
        end
    else
        for j = 1:T-1
            denom(j) = (1/2*rho*Area*v_int(j)^2*v(j+1));
        end
        [ordine_scarto,ordine_scarto_vecchio,Cd_spe_reg] = cdspe(scarto,ordine_scarto,Ec,Ed_corr,denom);        
        for j=1:T-1
            Ed_stoch(j) = 1/2*Area*rho*ppval(PP,v_int(j))*v_int(j)^2*v(j+1);
        end
    end
     

    
    % stima fattori correttivi
    Ed = Ed_stoch;
    Er = Er_corr;

    A = [Ed' Er'];
    for j=1:T-1
          B(j) = Ec(j) - Ec(j+1) + E_ruote(j)-E_ruote(j+1) + Ep(j) + W_int(j)*rend; %  
    end
    
    c = A(int_inizio:int_fine,:)\B(int_inizio:int_fine); % Ax = b dove x_1 = coeff_corr_cd , x_2 
    c_prod = c_prod*c(2); 

% Campionamento (downsampling)

param_smooth_2 = 5;
W_smooth = smooth(W_int,param_smooth_2);
testo = "W (media mobile " + param_smooth_2 + "s)";


figure('NumberTitle', 'off', 'Name', 'Grafico Cd sperimentale') 
grid on
yyaxis left
plot(v_int(int_inizio+lung:int_fine),ppval(PP,v_int(int_inizio+lung:int_fine)),'b') 
hold on
plot(v_int(int_inizio+lung:int_fine),c(1)*ppval(PP,v_int(int_inizio+lung:int_fine)),'g')
hold on
plot(v_int(int_inizio+lung:int_fine),Cd_spe_reg(1:int_fine-int_inizio-lung+1),'o')
hold on
ylabel('Cd speri')
xlabel('Velocità (m/s)') 
axis([10 26 0.00 0.075])
yyaxis right
plot(v_int(int_inizio+lung:int_fine),W_smooth(int_inizio+lung:int_fine),'.m')
axis([10 26 150 400])
ylabel('Potenza')
hold on

lgd = legend('Cd di sim CFD non corretto','Cd di sim CFD corretto',...
    'Cd spe puntuale','Potenza');
lgd.Location = 'north';
grid on

figure('NumberTitle', 'off', 'Name', 'Distribuzione ordine scarto (pre-filter)')
scatter(v_int,ordine_scarto_vecchio)
hold on
xlabel('Velocità')
ylabel('Ordine scarto (pre-filter')
grid on

figure('NumberTitle', 'off', 'Name', 'Distribuzione ordine scarto (post-filter)')
scatter(v_int,ordine_scarto)
hold on
xlabel('Velocità')
ylabel('Ordine scarto (post-filter')
grid on
     


figure
%salvataggio coefficienti
fitv=0.1:0.1:40;
c_d=c(1)*ppval(PP,fitv);
c_r=c_prod*ppval(RR,fitv); 
M=[c_d',c_r',ones(400,1)*0.97];
nome_scrittura = 'coeff.csv';
csvwrite(nome_scrittura,M);



%% Determino posizione cambiate (sottraggo -1 rispetto alla componente del vettore cad)
pos_camb = [21 38 49 65 83 109 128 157 191 232]; % venerdì PM (BM 2019)
% pos_camb = [22 33 45 62 80 104 124 144 186 235]; % giov PM (BM2019) 
v_pos_camb = v_int(pos_camb);
y_pos_camb = 0.025*ones(1,length(pos_camb));
end
