%% ------Simulink model------ %

clear
close all
clc

%% Bike Parameters

% Bike selection
bikeChoice = menu('Choose a Bike', 'Phoenix', 'Taurus', 'Cerberus');

%Bike Parameters Phoenix
%Aerodynamics
L = 2.63; %[m] Length of the fairing in the direction of flow
CxA_ref = 0.010344; %[m^2] CdA as measured/simulated at some particular speed
v_ref = 33.3333; %[m/s] Speed at which CdA has been specified
V_vec = [30:10:100 105:5:150]/3.6;
Cx_vec = [0.04179 0.03765 0.03503 0.03315 0.03172 0.03058 0.02981 0.02972 0.02972 0.02981 0.03010 0.03061 0.03133 0.03255 0.03397 0.03517 0.03648 0.03770];
A = 0.2732;

%Inertia
mv = 28; %[kg] Mass of vehicle excluding wheels
mr = 48; %[kg] Mass of rider, shoes, clothing, etc.
mw = 3; %[kg] Total mass of all wheels
m = mv+mr+mw;
me = mr+mv+mw*1.5; %[kg] Equivalent mass

%Mechanical
eta_tot = 0.97; %End-to-end efficiency of drivetrain
crr_1 = 0.0013; %Constant coefficient rolling resistance
crr_2 = 0.000038; %Linear coefficient rolling resistance
%tau_tot = 0.175; %Rapporto di trasmissione totale
R_wheel = 0.23157; %[m] Raggio ruota
n_start = 0;

% Override values for Taurus if selected
if bikeChoice == 2

    %Bike Parameters Taurus
    %Aerodynamics
    L = 2.63; %[m] Length of the fairing in the direction of flow
    CxA_ref = 0.0127; %[m^2] CdA as measured/simulated at some particular speed
    v_ref = 33.3333; %[m/s] Speed at which CdA has been specified
    V_vec = [30:10:100 105:5:150]/3.6;
    Cx_vec = [0.04047 0.03601 0.03308 0.03102 0.02973 0.03069 0.03548 0.03758 0.03778 0.03792 0.03817 0.03852 0.03901 0.03986 0.04076 0.04097 0.04120 0.04124];
    A = 0.28432;

    %Inertia
    mv = 28; %[kg] Mass of vehicle excluding wheels
    mr = 60; %[kg] Mass of rider, shoes, clothing, etc.
    mw = 3; %[kg] Total mass of all wheels
    m = mv+mr+mw;
    me = mr+mv+mw*1.5; %[kg] Equivalent mass

    %Mechanical
    eta_tot = 0.97; %End-to-end efficiency of drivetrain
    crr_1 = 0.0012; %Constant coefficient rolling resistance
    crr_2 = 0.000038; %Linear coefficient rolling resistance
    %tau_tot = 0.175; %Rapporto di trasmissione totale
    R_wheel = 0.18; %[m] Raggio ruota
    n_start = 0;

end

% Override values for Cerberus if selected
if bikeChoice == 3

    %Bike Parameters Taurus
    %Aerodynamics
    L = 2.80; %[m] Length of the fairing in the direction of flow
    CxA_ref = 0.01836; %[m^2] CdA as measured/simulated at some particular speed
    v_ref = 27.78; %[m/s] Speed at which CdA has been specified

    %Inertia
    mv = 30; %[kg] Mass of vehicle excluding wheels
    mr = 68; %[kg] Mass of rider, shoes, clothing, etc.
    mw = 4.5; %[kg] Total mass of all wheels
    m = mv+mr+mw;
    me = mr+mv+mw*1.5; %[kg] Equivalent mass

    %Mechanical
    eta_tot = 0.97; %End-to-end efficiency of drivetrain
    crr_1 = 0.0012; %Constant coefficient rolling resistance
    crr_2 = 0.000038; %Linear coefficient rolling resistance
    %tau_tot = 0.175; %Rapporto di trasmissione totale
    R_wheel = 0.23157; %[m] Raggio ruota
    n_start = 0;

end

%% Load Run and extract input vectors

UIControl_FontSize_bak = get(0, 'DefaultUIControlFontSize');
% Set a larger font size for the menu
set(0, 'DefaultUIControlFontSize', 18);
switch bikeChoice
    case 1
        % Sub-menu for Phoenix
        subCaseMenu = menu('Choose a Run','Matilde_12_09_2023_PM','Matilde_13_09_2023_AM','Matilde_14_09_2023_AM','Matilde_15_09_2023_AM');
      
        switch subCaseMenu
            case 1

                tabella_dati = readtable('Matilde_12_09_2023_PM.csv');
                Cadence_vector = tabella_dati.cadence(5:end);
                Power_vector = tabella_dati.power(5:end);
                Speed_vector = tabella_dati.speed(5:end);

            case 2

                tabella_dati = readtable('Matilde_13_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(4:end);
                Power_vector = tabella_dati.power(4:end);
                Speed_vector = tabella_dati.speed(4:end);

            case 3

                tabella_dati = readtable('Matilde_14_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(2:end);
                Power_vector = tabella_dati.power(2:end);
                Speed_vector = tabella_dati.speed(2:end);

            case 4

                tabella_dati = readtable('Matilde_15_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(4:end);
                Power_vector = tabella_dati.power(4:end);
                Speed_vector = tabella_dati.speed(4:end);

        end


    case 2
        % Sub-menu for Taurus
        subCaseMenu = menu('Choose a Run', 'BM18_day1_AM_short','BM18_day1_PM','BM18_day2_PM','BM18_day4_AM','BM18_day4_PM','BM18_day5_AM','BM18_day5_PM','BM18_day6_AM','BM_19_Friday_PM_Andrea','BM_19_Monday_AM_Andrea','BM_19_Monday_PM_Andrea','BM_19_Sunday_PM_Andrea','BM_19_Thursday_PM_Andrea','BM_19_Tuesday_AM_Andrea');

        switch subCaseMenu
            case 1

                tabella_dati = readtable('BM18_day1_AM_short.csv');
                Cadence_vector = tabella_dati.Cadence(6:end);
                Power_vector = tabella_dati.Watts(6:end);
                Speed_vector = tabella_dati.Km_h(6:end);

            case 2


                tabella_dati = readtable('BM18_day1_PM.csv');
                Cadence_vector = tabella_dati.Cadence(10:end);
                Power_vector = tabella_dati.Watts(10:end);
                Speed_vector = tabella_dati.Km_h(10:end);

            case 3

                tabella_dati = readtable('BM18_day2_PM');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

            case 4

                tabella_dati = readtable('BM18_day4_AM');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

            case 5

                tabella_dati = readtable('BM18_day4_PM');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

            case 6

                tabella_dati = readtable('BM18_day5_AM');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

            case 7

                tabella_dati = readtable('BM18_day5_PM');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

            case 8

                tabella_dati = readtable('BM18_day6_AM.csv');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

                case 9

                tabella_dati = readtable('BM_19_Friday_PM_Andrea.csv');
                Cadence_vector = tabella_dati.Var6;
                Power_vector = tabella_dati.Var4;
                Speed_vector = tabella_dati.Var3;

                case 10

                tabella_dati = readtable('BM_19_Monday_AM_Andrea.csv');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

                case 11

                tabella_dati = readtable('BM_19_Monday_PM_Andrea.csv');
                Cadence_vector = tabella_dati.Var6;
                Power_vector = tabella_dati.Var4;
                Speed_vector = tabella_dati.Var3;

                case 12

                tabella_dati = readtable('BM_19_Sunday_PM_Andrea.csv');
                Cadence_vector = tabella_dati.Var6;
                Power_vector = tabella_dati.Var4;
                Speed_vector = tabella_dati.Var3;

                case 13

                tabella_dati = readtable('BM_19_Thursday_PM_Andrea.csv');
                Cadence_vector = tabella_dati.Var6;
                Power_vector = tabella_dati.Var4;
                Speed_vector = tabella_dati.Var3;

                case 14

                tabella_dati = readtable('BM_19_Tuesday_AM_Andrea.csv');
                Cadence_vector = tabella_dati.Cadence;
                Power_vector = tabella_dati.Watts;
                Speed_vector = tabella_dati.Km_h;

            otherwise
                disp('Invalid selection.');
        end
    case 3
        % Sub-menu for Cerberus
        subCaseMenu = menu('Choose a Run','Diego_12_09_2023_AM','Diego_13_09_2023_AM','Diego_15_09_2023_AM','Diego_15_09_2023_PM','Diego_16_09_2023_AM');
    
        switch subCaseMenu
            case 1

                tabella_dati = readtable('Diego_12_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(5:end);
                Power_vector = tabella_dati.power(5:end);
                Speed_vector = tabella_dati.speed(5:end);

            case 2

                tabella_dati = readtable('Diego_13_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(4:end);
                Power_vector = tabella_dati.power(4:end);
                Speed_vector = tabella_dati.speed(4:end);

            case 3

                tabella_dati = readtable('Diego_15_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(2:end);
                Power_vector = tabella_dati.power(2:end);
                Speed_vector = tabella_dati.speed(2:end);

            case 4

                tabella_dati = readtable('Diego_15_09_2023_PM.csv');
                Cadence_vector = tabella_dati.cadence(4:end);
                Power_vector = tabella_dati.power(4:end);
                Speed_vector = tabella_dati.speed(4:end);

            case 5

                tabella_dati = readtable('Diego_16_09_2023_AM.csv');
                Cadence_vector = tabella_dati.cadence(4:end);
                Power_vector = tabella_dati.power(4:end);
                Speed_vector = tabella_dati.speed(4:end);

        end
end
% Restore the original font size
set(0, 'DefaultUIControlFontSize', UIControl_FontSize_bak);

%% Physiscal Constants

g = 9.81; %[m/s^2] Gravity
mu = 0.0000198; %[Pas] Viscosity of air
rho = 0.97; %[kgm^3] Density of air

%% Simulation

t_final = length(Cadence_vector); %[s] Ride Duration
time_vec = linspace(0,t_final,length(Cadence_vector))';
v_init = Speed_vector(2)/3.6; %[m/s] Velocità iniziale
Cadence_vector = [time_vec,Cadence_vector];
Power_vector = [time_vec,Power_vector];
Speed_vector = [time_vec,Speed_vector];
open model_simulink_OLD
sim model_simulink_OLD

%% Dissipation ratio

Linear_speed_ratio = speed_detect.Data./speed_theory.Data;
Parabolic_speed_ratio = (speed_detect.Data+speed_detect.Data.^2)./(speed_theory.Data+speed_theory.Data.^2);
Acc_ratio = acc_detect.Data./acc_theory.Data;
Space_ratio = space_detect.Data(end)./space_theory.Data(end);
Net_Power_ratio = acc_detect.Data.*speed_detect.Data./acc_theory.Data.*speed_theory.Data;
Space_Integral_Speed_ratio = trapz(space_detect.Data,speed_detect.Data)/trapz(space_theory.Data,speed_theory.Data);
Space_Integral_Speed_complete_ratio = trapz(space_detect.Data,speed_detect.Data+speed_detect.Data.^2)/trapz(space_theory.Data,speed_theory.Data+speed_theory.Data.^2);
Space_Integral_Acc_ratio = trapz(space_detect.Data,acc_detect.Data)/trapz(space_theory.Data,acc_theory.Data);
Space_Integral_NetPower_ratio = trapz(space_detect.Data,acc_detect.Data.*speed_detect.Data)./trapz(space_theory.Data,acc_theory.Data.*speed_theory.Data);
Time_Integral_NetPower_ratio = trapz(acc_detect.Time,acc_detect.Data.*speed_detect.Data)./trapz(acc_theory.Time,acc_theory.Data.*speed_theory.Data);

figure;
title('Dissipation Ratio')
hold all
plot(Linear_speed_ratio,'LineWidth',2)
plot(Parabolic_speed_ratio,'LineWidth',2)
% plot(Acc_ratio)
plot(Space_ratio*ones(length(Linear_speed_ratio),1),'LineWidth',2)
% plot(Net_Power_ratio)
plot(Space_Integral_Speed_ratio*ones(length(Linear_speed_ratio),1),'LineWidth',2)
plot(Space_Integral_Acc_ratio*ones(length(Linear_speed_ratio),1),'LineWidth',2)
plot(Space_Integral_NetPower_ratio*ones(length(Linear_speed_ratio),1),'LineWidth',2)
plot(Time_Integral_NetPower_ratio*ones(length(Linear_speed_ratio),1),'LineWidth',2)
plot(Space_Integral_Speed_complete_ratio*ones(length(Linear_speed_ratio),1),'LineWidth',2)
grid on
xlabel('Simulink Samples')
legend('Linear_speed_ratio','Parabolic_speed_ratio','Space_ratio','Space_Integral_Speed_ratio','Space_Integral_Acc_ratio','Space_Integral_NetPower_ratio','Time_Integral_NetPower_ratio','Space_Integral_Speed_complete_ratio')