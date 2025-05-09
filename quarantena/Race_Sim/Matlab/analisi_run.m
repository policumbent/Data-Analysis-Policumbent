function [P] = analisi_run(IdRun)

[~,~,~,~,~,~,~,~,FileName] = readFile(IdRun);

data=csvread(FileName,1,0); %1a riga del csv è riga 0, 1a riga di un vettore è riga 1 
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
P = zeros(1,6);
% determino medie di potenza sugli intervalli
P(1) = mean(data(1:indice(1),4)); 
P(2) = mean(data(indice(1)+1:indice(2),4));
P(3) = mean(data(indice(2)+1:indice(3),4));
P(4) = mean(data(indice(3)+1:indice(4),4)); 
P(5) = mean(data(indice(4)+1:indice(5),4)); 
P(6) = mean(data(indice(5)+1:N,4));

% Medie su 3s
P_allungata = [0; data((1:end),4); 0];
for i=2:length(data((1:end),5))-1
           P_med_3s(i) = sum(P_allungata(i-1:i+1)/3); % cambiare in media centrata
end
P_med_3s(1) = P_med_3s(2);
P_med_3s(length(data((1:end),5))) = P_med_3s(length(data((1:end),5))-1);


% determino accelerazione e acc. mediata su 3s
for i=1:N-1
        a(i) = data(i+1,3) - data(i,3); % sarebbe diviso 1
end
a_allungata = [0;a';0];

for i = 2:length(data((1:end),5))-1
         a_med_3s(i) = sum(a_allungata(i-1:i+1)/3);
end

ax1 = subplot(3,1,[1,2]);
plot(data((1:end),5),data((1:end),3),data((1:end),5),P_med_3s,data((1:end),5),data((1:end),7),data((1:end),5),data((1:end),6));
legend('Velocità [km/h]','Potenza immessa mediata su 3s [W]','Hrate','Cadenza','Location','north');
xlabel('Distanza (km)');
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



end