
function [time,vel,power,dist,Hrate] = readRaceCer(IDRun)

IDRun = append(IDRun,".csv");

% Read data from the run file (.csv)
table = readmatrix(IDRun);

% Initialize all the variables red from the table
timeMin = table(:,1);
Lngth = size(timeMin,1);
time = 1:Lngth;
vel = table(:,2);           % Velocity
power = table(:,6);         % Power
dist = table(:,3);           % Pedals RPM
Hrate = table(:,7);         % Heartrate

end 