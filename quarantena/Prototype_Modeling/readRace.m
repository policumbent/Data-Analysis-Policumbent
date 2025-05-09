function [altitude,cadence,distance,vel_lin,power] = readRace(IDRun)

IDRun = append(IDRun,".csv");

% Read data from the run file (.csv)
table = readmatrix(IDRun);

% Initialize all the variables red from the table
altitude = table(:,2);
cadence = table(:,3);
distance = table(:,4);
vel_lin = table(:,5);
power = table(:,6);

end 

