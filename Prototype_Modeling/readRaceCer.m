
function [time,vel,power,dist,Hrate,RPM] = readRaceCer(IDRun)

IDRun = append(IDRun,".csv");

% Read data from the run file (.csv)
table = readmatrix(IDRun);

% Initialize all the variables red from the table
Lngth = size(table,1);
time = 1:Lngth;
Hrate = table(:,3);         % Heartrate
RPM = table(:,4);           % Cadence
dist = table(:,5);          % Pedals RPM
vel = table(:,6);           % Velocity
power = table(:,7);         % Power

end 