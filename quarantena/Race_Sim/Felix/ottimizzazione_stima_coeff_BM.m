
clear all
close all
clc

global v T km data;

% Preparativi
filename='prova.txt'; 
data=csvread(filename,1,0);     %leggo csv della prova (aggiungere 1,0 se necessario)
T=length(data(:,1));        %qtà di rilevazioni [adim]
v=data(:,3)/3.6;            %vettore delle velocità [m/s]
metri=data(:,5)*10^3;             %vettore delle distanze dal 1o rilevamento [m]
t=data(:,1);                %vettore dei tempi [s]
cad=data(:,6);              %vettore della cadenza [giri/min]
W = data(:,4);
vett_elevazione=data(:,9);
% pendenza = csvread('pendenza_migliorata.csv',0,0);
% pendenza = csvread('pendenza_nuova_media_viagg.csv',0,0);
% pendenza = csvread('pendenza_nuova_smooth_200_disl_redistr.csv',0,0);
pendenza = data(:,8);
% pendenza = csvread('pendenza_da_base_lagrangiana.csv',0,0);

%% Da impostare: cond. ambientali e dati veicolo
% (27°,22.5,863.6 per giov PM Andrea), (30°,20,861 per ven PM Andrea), 
% (22°,37,855 per lun PM Andrea), (28,25,863.8 per giov PM Vittoria),
% (30°,20,861 per ven PM Vittoria)
temp = 27;  
umid = 22.5;  
mbar = 863.6; 
raggio=0.23157; % Michelin Blue 8 bar (20')
% raggio=0.2291831; % Conti LTD 7 bar (20')
m=92; % 80 vittoria, 92 Andrea, 85 Phoenix
I = 0.044;
Area = 0.28432; % Taurus: 0.28432, Phoenix. 0.2732 
PP=interpolazione_CD_CFD;
RR=interpolazione_CR; 
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

% Correggo impostazione raggio ruota per lun PM
% metri = metri*1.011;
% v = v*1.011;

%% Determino integrali sugli intervalli/ potenza

vel_vento = 0;
v_int_con_vento = zeros(T-1,1);
cos_vento = - cos(45/360*2*pi);
% cos(10/360*2*pi) giov PM vento An, - cos(45/360*2*pi) per lun PM An,
% - cos(45/360*2*pi) per giov PM vento Vi, no vento per ven PM

% j indice sull'intervallo <-> invece indice i per l'i-esimo valore registrato in tempo
for j =1:T-1
            if j == 1
                      m1 = 1;
                      m2 = round(metri(2));
            else
                      m1 = round(metri(j));
                      m2 = round(metri(j+1));   
            end
                        
            % Determino velocità sull'intervallo
            if j > 2 && j < T-1
                W_int(j) = 1/3*(W(j-1)+W(j)+W(j+1));
            else
                W_int(j) = 0.5*(W(j)+W(j+1));
            end
            
            y =  1; % somma mi da dislivello totale dell'intervallo
            Ep(j) =  m*g*y; % pendenza favorevole immette sempre energia
            
            v_int(j) = 0.5*(v(j)+v(j+1));
            
            % uso della formula del trapezio come formula di quadratura
            v_int_con_vento(j) = 0.5*(v(j)+v(j+1)) + cos_vento*(vel_vento/3.6);
            Ed(j) = 1/2*Area*rho*ppval(PP,v_int_con_vento(j))*v_int_con_vento(j)^2*v(j+1);
            Er(j) =  m*g*ppval(RR,v_int(j))*v(j+1);
end

%%  Determino valori scalari
for i = 1:T
            Ec(i) = 1/2*m*v(i)^2;   
            E_ruote(i)  = I*(v(i)/raggio)^2;       
end


%% Determino A,B e stima
A = [Ed' Er'];

B = zeros(T-1,1);
for j=1:T-1
          B(j) = Ec(j) - Ec(j+1) + E_ruote(j)-E_ruote(j+1) + W_int(j)*rend; %  
end

% Impostazione intervallo di fine/ inizio alternativi
int_fine = 283;
% int_fine = 283; % per giov PM (correctio: ha senso mettere sempre T-1)
int_inizio = find(v>10);
int_inizio = int_inizio(1);
%int_fine = find(v>(120/3.6));
%int_fine = int_fine(1);
          
c = A(int_inizio:int_fine,:)\B(int_inizio:int_fine); % Ax = b dove x_1 = coeff_corr_cd , x_2 
Ed_corr = Ed*c(1);
Er_corr = Er*c(2);

% z = optimvar('z');
% c1 = optimvar('c1');
% c2 = optimvar('c2');
% prob = optimproblem;
% prob.Objective = z;
% prob.Constraints.cons1 = B - Ed'*c1 - Er'*c2 <= z; 
% prob.Constraints.cons2 = -(B - Ed'*c1 - Er'*c2) <= z;
% prob.Constraints.cons3 = c1 <= 1.1;
% prob.Constraints.cons4 = c2 <= 1.1;
% prob.Constraints.cons5 = c1 >= 0.85;
% prob.Constraints.cons6 = c2 >= 0.85;
%  
% sol = solve(prob) 
%  
% Ed_corr = Ed*c1;
% Er_corr = Er*c2;

%salvataggio coefficienti
% fitv=0.1:0.1:40;
% c_d=c(1)*ppval(PP,fitv);
% c_r=c(2)*ppval(RR,fitv); 
% 
% M=[c_d',c_r',ones(400,1)*0.97];
% nome_scrittura = 'coeff_raff_no_stoch_no_iter_BM19_Giov_PM_Andrea_con_vento_angolo_cost.csv';
% csvwrite(nome_scrittura,M);


%% Determino scarto e ordine scarto

ordine_scarto = zeros(1,T-1);
scarto=zeros(1,T-1);
contatore_001 = 0;
for j=1:T-1
      scarto(j)= Ec(j) - Ec(j+1) + E_ruote(j)-E_ruote(j+1) + W_int(j)*rend ...
                      - Ed_corr(j) - Er_corr(j);
      
      ordine_scarto(j) = (scarto(j)/Ec(j+1));
    
    if ordine_scarto(j) > 0.01 && j<T
         contatore_001 = contatore_001 + 1;
    end
end
somma_scarto_con_fatt_correttivi = sum(abs(scarto));

% figure('NumberTitle', 'off', 'Name', 'Grafico Scarto')
% plot(metri(2:end)',scarto,'r')
% grid on
% xlabel('Metri')
% ylabel('Scarto')
% 
% figure('NumberTitle', 'off', 'Name', 'Grafico Ordine Scarto')
% plot(metri(2:end)',ordine_scarto)
% grid on
% xlabel('Metri')
% ylabel('Ordine Scarto')


%% Determino posizione cambiate (sottraggo -1 rispetto alla componente del vettore cad)
pos_camb = [21 38 49 65 83 109 128 157 191 232]; % venerdì PM (BM 2019)
%pos_camb = [22 33 45 62 80 104 124 144 186 235]; % giov PM (BM2019) 
v_pos_camb = v_int(pos_camb);
y_pos_camb = 0.025*ones(1,length(pos_camb));

%% Ricavo Cd sperimentale: Metodo 2bis
scarto_vecchio = scarto;
ordine_scarto_vecchio = ordine_scarto;

% passo 1: filtro segnali ad alta frequenza
lung = 10;
d = lung;
s = 0;
e = 0;
vett_ind_filtrato = zeros(1,T-1);
jj = 1;

for j = 1:T-1
    % Determino media
    if j <= lung
        media = mean(abs(ordine_scarto(j:j+lung))); 
    elseif j>lung && j<=2*lung
        media = mean(abs(ordine_scarto(j-e:j+lung)));
        e = e+1;
    elseif j >= T-1-lung
        media = mean(abs(ordine_scarto(j-lung:T-1)));
    else
        media = mean(abs(ordine_scarto(j-lung:j+lung)));
    end
   
%    % Filtro 1: verifico che entrambi gli ordini scarto siano sopra la
%    % media e di segno diverso
%     if j < T-3
%         if abs(ordine_scarto(j)) > media && abs(ordine_scarto(j+1)) > media
%              if sign(ordine_scarto(j)) ~= sign(ordine_scarto(j+1)) 
%                 scarto(j:j+1) = mean(ordine_scarto(j:j+2))*Ec(j+1:j+2);
%                 ordine_scarto(j:j+1) = mean(scarto(j:j+2)/Ec(j+1:j+3));  
%             end
%         end
%     end
  

 % Filtro 2: smorziamo abbastanza
%     if j < T-3
%         if abs(ordine_scarto(j)) > media && sign(ordine_scarto(j)) ~= sign(ordine_scarto(j+1))
%             scarto(j:j+1) = mean(ordine_scarto(j:j+2))*Ec(j+1:j+2);
%             ordine_scarto(j:j+1) = mean(scarto(j:j+2)/Ec(j+1:j+3));
%         end
%     end


% Filtro 3: via di mezzo ponendo condizione minima sull'intervallo
% successivo -> non smorza picco iniziale
%     if j < T-3
%         if abs(ordine_scarto(j)) > media && abs(ordine_scarto(j+1)) > 0.2*media && ...
%                 sign(ordine_scarto(j)) ~= sign(ordine_scarto(j+1))
%             scarto(j:j+1) = mean(ordine_scarto(j:j+2))*Ec(j+1:j+2);
%             ordine_scarto(j:j+1) = mean(scarto(j:j+2)/Ec(j+1:j+3));
%         end
%     end
     

% Filtro 4: filtro combinato, cioe applico filtro 2 per j < lung, dopodiché
% applico filtro 1
% 
    if j < 1.5*lung % Filtro 2
        if abs(ordine_scarto(j)) > media && sign(ordine_scarto(j)) ~= sign(ordine_scarto(j+1))
            scarto(j:j+1) = mean(ordine_scarto(j:j+2))*Ec(j+1:j+2);
            ordine_scarto(j:j+1) = mean(scarto(j:j+2)/Ec(j+1:j+3)); % aggiorno ordine scarto
            %j 
            j = j+1;
        else
            vett_ind_filtrato(jj) = j;
            
            if j~=T-1
                jj = jj+1;
            end
        end
    elseif j < T-3 % Filtro 1
        if abs(ordine_scarto(j)) > media && abs(ordine_scarto(j+1)) > media && ...
                sign(ordine_scarto(j)) ~= sign(ordine_scarto(j+1)) 
                    scarto(j:j+1) = mean(ordine_scarto(j:j+2))*Ec(j+1:j+2);
                    ordine_scarto(j:j+1) = mean(scarto(j:j+2)/Ec(j+1:j+3)); % aggiorno ordine scarto
                    %j 
                    j = j+1;
        else
            vett_ind_filtrato(jj) = j;
            
            if j~=T-1
                jj = jj+1;
            end
        end
        
    end

end


% passo 2: considero se errore maggiore o minore dell'errore medio ed ev. sottraggo questo 
% lung = 10;
d = 10;
s = 0;
e = 0;
param_1 = 0; 
param_3 = 1.5; % rateo per soglia superiore dell'errore da considerare rispetto all'errore medio
param_4 = 1; % rateo moltiplicato che va a moltiplicarsi per la media che detraggo

for j = 1:T-1    
    
    % determino media ordine_scarto
    if j <= lung
        media = mean(abs(ordine_scarto(j:j+lung))); 
    elseif j>lung && j<=2*lung
        media = mean(abs(ordine_scarto(j-e:j+lung)));
        e = e+1;
    elseif j >= T-1-lung
        media = mean(abs(ordine_scarto(j-lung:T-1)));
    else
        media = mean(abs(ordine_scarto(j-lung:j+lung)));
    end
    
    % detraggo errore medio se scarto oltre scarto medio
    if abs(scarto(j)) < param_4*media*Ec(j+1)
        scarto(j) = param_1*scarto(j); 
    elseif abs(scarto(j)) >= param_4*media*Ec(j+1) && abs(scarto(j)) < param_3*media*Ec(j+1)
        scarto(j) = scarto(j) - sign(scarto(j))*param_4*media*Ec(j+1); 
    else
        scarto(j) = sign(scarto(j))*param_3*media*Ec(j+1) - sign(scarto(j))*param_4*media*Ec(j+1); 
    end
end

Cd_spe = zeros(1,T-1);
for j=1:T-1
    Cd_spe(j) = (scarto(j)+Ed_corr(j))/(1/2*rho*Area*v_int(j)^2*v(j+1));
end

% passo 3: Regolarizzazione Cd spe
lung = 10; % standard: 10
n_int = 5; % standard: 5
e = 0;

% 
% 
% M = 10;
% h = 1/M*ones(1,M);
% Cd_spe_reg = conv2(Cd_spe(int_inizio:int_fine),h,'valid');

Cd_spe_reg = zeros(1,int_fine-int_inizio+1);
for j = 1:T-1
    
    ordine_scarto(j) = scarto(j)/Ec(j+1); 
    
    % Filtro di media mobile 
    if j <= lung
        Cd_spe_reg(j) = mean(abs(Cd_spe(j:j+n_int)));
    elseif j>lung && j<=lung + n_int
        Cd_spe_reg(j) = mean(abs(Cd_spe(j-e:j+n_int))); 
        e = e+1;
    elseif j >= T-1-n_int
        Cd_spe_reg(j) = mean(abs(Cd_spe(j-n_int:T-1)));
    else
        Cd_spe_reg(j) = mean(abs(Cd_spe(j-n_int:j+n_int)));
    end

end

% Alternativa: leaky integrator
% Cd_spe_reg = zeros(1,int_fine-int_inizio+1);
% lambda = 0.9;
% h = zeros(1,lung);
% 
% h(1) = 1-lambda;
% for k=1:lung-1
%         h(1+k) = lambda^k*h(1);
% end
%   
% k = 1;
% for n=1:int_fine-int_inizio+1
%     
%     j = 1;
%     while j<=lung-1
%         Cd_spe_reg(n) = Cd_spe_reg(n) + h(j)*Cd_spe(int_inizio+n-j);
%         j = j+1;
%     end
%       
% end

%Passo 4: campionamento
passo = 25; % standard: 25
vett_v = zeros(1,floor((int_fine-int_inizio+1)/passo));
vett_Cd = zeros(1,floor((int_fine-int_inizio+1)/passo)); 
i = int_inizio;  

for j=1:15 %floor((int_fine-int_inizio+1)/passo)
    vett_v(j) = v_int(i); 
    vett_Cd(j) = Cd_spe_reg(i);
    
    % passo var 2
    if v_int(i)>25 && v_int(i)<=30 
        passo = 30;
    elseif v_int(i)>30 
        passo = 35;
    end
    
    i = i+passo
     
    if i>int_fine
        j_finale = j; % non scelgo punti oltre 33 m/s
        break 
    end
    
end

p_spe_pol = pchip(vett_v(1:j_finale)',vett_Cd(1:j_finale)');
pp_spe_pol = ppval(p_spe_pol,v_int');

% frame di Gabor (traslate di gaussiane modulate)
p_spe = fit(v_int(int_inizio:int_fine)',Cd_spe_reg(int_inizio:int_fine)','gauss3');
pp_spe = p_spe(v_int')

scatter(v_int',pp_spe_pol')
hold on
scatter(v_int',pp_spe')
legend('Approssimazione polinomiale','Approssimazione mediante gaussiane')

% Aggiorno l'errore
Ed_spe = zeros(1,T-1);
scarto_ass = zeros(1,T-1);
for i=1:jj-1
    j = vett_ind_filtrato(i);
    Ed_spe(j) = 1/2*Area*rho*pp_spe(j)*v_int(j)^2*v(j+1);
    scarto_ass(j)= Ec(j) - Ec(j+1) + E_ruote(j)-E_ruote(j+1) + W_int(j)*rend ...
                      - Ed_spe(j) - Er_corr(j);
end

somma_scarto_con_cd_sper = sum(abs(scarto_ass));

param_smooth_2 = 5;
W_smooth = smooth(W_int,param_smooth_2);
testo = "W (media mobile " + param_smooth_2 + "s)";
testo = char(testo);

param_smooth_3 = 5;
Ep_smooth = smooth(Ep,param_smooth_3);
testo_2 = "Epot (media mobile " + param_smooth_3 + "s)";
testo_2 = char(testo_2);

% Plot Cd speri
figure('NumberTitle', 'off', 'Name', 'Grafico Cd sperimentale') 
yyaxis left
plot(v_int,ppval(PP,v_int),'b') 
hold on
plot(v_int,c(1)*ppval(PP,v_int),'g')
hold on
plot(v_int',pp_spe_pol,'k')
hold on
plot(v_int',pp_spe','b')
hold on
scatter(v_int(int_inizio:int_fine),Cd_spe_reg(int_inizio:int_fine),'r')
hold on
plot(vett_v,vett_Cd,'k*')
ylabel('Cd')
axis([0 40 0.00 0.055])
hold on
plot(v_pos_camb',y_pos_camb, 'color', 'blue', 'marker',  'o', 'markerfacecolor',  'blue', 'markersize', 3) 
yyaxis right
plot(v_int,W_smooth,'.m')
hold on
plot(v_int,Ep_smooth,'.c')
axis([0 40 50 500])
lgd = legend('Cd di sim CFD non corretto','Cd appross (minimi quadrati)','Cd spe appross (polinomio ortogonale)',...
     'Cd spe approssimato (gaussiane)','Cd spe puntuale (intervallo)','Cd spe campionato','posizione cambiate',testo,testo_2)
lgd.Location = 'north'
xlabel('Velocità (m/s)') 
ylabel('Potenza')
grid on

figure('NumberTitle', 'off', 'Name', 'Distribuzione ordine scarto (pre-filter)')
scatter(scarto_vecchio,ordine_scarto_vecchio)
hold on
xlabel('Scarto (pre-filter)')
ylabel('Ordine scarto (pre-filter')
grid on

figure('NumberTitle', 'off', 'Name', 'Distribuzione ordine scarto (post-filter)')
scatter(scarto,ordine_scarto)
hold on
xlabel('Scarto (pre-filter)')
ylabel('Ordine scarto (pre-filter')
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

% Plot per articolo
% figure('NumberTitle', 'off', 'Name', 'Grafico Cd sperimentale') 
% plot(v_int,1.35*ppval(PP,v_int),'b') 
% hold on
% plot(v_int,1.35*pp_spe,'k')
% hold on
% plot(vett_v,1.35*vett_Cd,'k*')
% legend('Cd (CFD simulation)','Cd (experimental data)') 
% xlabel('Velocità (m/s)') 
% ylabel('Cd') 
% grid on


%salvataggio coefficienti
% fitv=0.1:0.1:40;
% c_d=ppval(p_spe,fitv);
% c_r=c(2)*ppval(RR,fitv); 
% Ed_corr = Ed*c(1);
% Er_corr = Er*c(2);
%  
% M=[c_d',c_r',ones(400,1)*0.97];
% nome_scrittura = 'coeff_raff_ottimizzazione_smooth_100_no_anticipo_BM19_ven_PM_fine_anticipata.csv';
% csvwrite(nome_scrittura,M);



