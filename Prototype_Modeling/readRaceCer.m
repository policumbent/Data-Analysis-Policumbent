
function [time,vel,power,dist,Hrate,RPM] = readRaceCer(IDRun)

IDRun = append(IDRun,".csv");

% Read data from the run file (.csv)
table = readmatrix(IDRun);

% Initialize all the variables red from the table
timeMin = table(:,1);
Lngth = size(timeMin,1);
time = 1:Lngth;
vel = table(:,6); % Velocity
RPM = table(:,4);
power = table(:,7);         % Power
dist = table(:,5);           % Pedals RPM
Hrate = table(:,3);         % Heartrate

end 