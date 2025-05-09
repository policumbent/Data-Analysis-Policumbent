clear 
close all
clc

%% Apertura file

fileList = { ...
    'Matilde_12_09_2023_PM.csv';
    'Matilde_13_09_2023_AM.csv';
    'Matilde_14_09_2023_AM.csv';
    'Matilde_15_09_2023_AM.csv'};

labels = {'12/09', '13/09', '14/09', '15/09'};
figure;
hold on


for i = 1:length(fileList)
    filename = fileList{i};
    
    data = readtable(filename);
    Pw = data.power(1:end);
    time = linspace(0, length(Pw), length(Pw));

    cp = polyfit(time', Pw, 3);
    yp = polyval(cp, time);

    h(i) = plot(time, yp, 'LineWidth', 1.5);

end

legend(h, labels, 'Location', 'best');
xlabel('Tempo (s)');
ylabel('Potenza (W)');
title('Confronto potenza tra le run');
grid on;

