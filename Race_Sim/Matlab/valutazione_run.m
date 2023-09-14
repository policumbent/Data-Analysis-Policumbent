
clc
clear all
close all

%1a riga del csv è riga 0, 1a riga di un vettore è riga 1 
data=csvread('BM_19_Tuesday_AM_Andrea.csv',1,0);
P_med = mean(data((1:end),4));
P_max = max(data((1:end),4));
N = length(data(1:end,3));

% determino indice dei km
s=1;
indice = ones(5,1);


for i=1:N
        if data(i,5) > 0.5 & data(i,5) < 0.52
              indice(1) = i;    
        end
        
         if data(i,5) > 1.5 & data(i,5) < 1.53
              indice(2) = i;
         end
        
          if data(i,5) > 3 & data(i,5) < 3.05
              indice(3) = i;
          end
                 
         if data(i,5) > 5 & data(i,5) < 5.05
              indice(4) = i;
         end
         
          if data(i,5) > 7 & data(i,5) < 7.05
              indice(5) = i;
         end
end

% determino medie sugli intervalli
P_0_05 = mean(data(1:(indice(1)),4)); 
P_05_15 = mean(data((indice(1)+1:indice(2)),4));
P_15_3 = mean(data((indice(2)+1:indice(3)),4));
P_3_5 = mean(data((indice(3)+1:indice(4)),4)); 
P_5_7 = mean(data((indice(4)+1:indice(5)),4)); 

% Potenza mediata su 3s
P_allungata = [0; 0; data((1:end),4); 0; 0];
for i=1:length(data((1:end),5))
           P_med_3s(i) = sum(P_allungata(i:i+2)/3);
end

% Acc. mediata su 3s
for i=1:N-1
        a(i) = (data(i+1,3) - data(i,3))/3.6; % sarebbe diviso 1
end
a_allungata = [0;0;a';0;0];

for i = 1:length(a)
         a_med_3s(i) = sum(a_allungata(i:i+2)/3);
end

ax1 = subplot(3,1,[1,2]);
plot(data((1:end),5),data((1:end),3),data((1:end),5),P_med_3s,data((1:end),5),data((1:end),7),data((1:end),5),data((1:end),6));
legend('Velocità [km/h]','Potenza immessa mediata su 3s [W]','Hrate','Cadenza','Location','north');
xlabel('Spazio (km)');
grid on
ylim = ([0 450]);


ax2 = subplot(3,1,3);
x2 = data(2:end,5);
plot(x2,a_med_3s);
legend('Accelerazione mediata su 3s (m/s)','Location','north');
xlabel('Spazio (km)');
grid on
ylim = ([0 4]);


% Lettura file di simulazione
% data=csvread('Andrea.csv',0,0);
% N = length(length(data(1:end,1)))
% p_med = mean(data((1:end),3));
% 
% figure
% plot(data((1:end),1),data((1:end),2)*3.6,data((1:end),1),data((1:end),3));
% legend('Velocità','Potenza immessa (W)');
% grid on
% xlabel('Spazio (km)');



