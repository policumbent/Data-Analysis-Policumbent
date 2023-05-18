function [time,torq,vel,power,dist,RPM,Hrate,Alt] = readRace(IDRun)

% Read data from the run file (.csv)
table = readmatrix(IDRun);

% Initialize all the variables red from the table
timeMin = table(:,1);
Lngth = size(timeMin,1);
time = (timeMin-ones(Lngth,1)*(timeMin(1)))*60;
torq = table(:,2);          % Torque
vel = table(:,3);           % Velocity
power = table(:,4);         % Power
dist = table(:,5);          % Distance
RPM = table(:,6);           % Pedals RPM
Hrate = table(:,7);         % Heartrate
Alt = table(:,9);           % Altitude

end 
