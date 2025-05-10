clear
close all
clc


%% creazione vettore potenza e tempo

file = 'Matilde_15_09_2023_AM.csv';

tabella_dati = readtable(file);
Pw = tabella_dati.power(3:end);
Vr = tabella_dati.speed(3:end);
Cd = tabella_dati.cadence(3:end);

t_final = length(Cd);
time = linspace(0, t_final, length(Cd))';

vel_reale = [time Vr];

cp = polyfit(time', Pw, 3);
yp = polyval(cp,time);

plot(time, Pw, time, yp)
title('potenza')
hold on

Power_vector = [time yp];

%% creazione vettore cadenza

coef = [1.8 1 0.782 0.470 -0.499 0.309 0.221 0.229 0.117 0.054];
n = length(coef);
c_min = [40 81 78 76 77 69 79 74 73 76];

delta_t = [29 7 11 19 3 49 34 35 75 81];

N_total = sum(delta_t);  % numero totale di campioni
x = zeros(1, N_total);
y = zeros(1, N_total);

idx = 1;  % indice di scrittura

for i = 1:n
    x_min = 0;
    x_max = delta_t(i);
    min_val = c_min(i);

    if i > 1
        c = min_val - coef(i) * x(idx - 1);
    else
        c = min_val;
    end

    f = @(xval) coef(i) * xval + c;

    x_i = linspace(x_min, x_max, delta_t(i));

    if i > 1
        x_i = x_i + x(idx - 1);
    end

    y_i = f(x_i);

    len = length(x_i);

    x(idx : idx + len - 1) = x_i;
    y(idx : idx + len - 1) = y_i;

    idx = idx + len;
end

Cadence_vector = [time y'];

plot(x, y, x, Cd);
title('cadenza');
hold on 




%% dati bici

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

% Physiscal Constants
g = 9.81; %[m/s^2] Gravity
mu = 0.0000198; %[Pas] Viscosity of air
rho = 0.97; %[kgm^3] Density of air

v_init = Vr(1)/3.6; %[m/s] Velocità iniziale


%% inizializza simulazione 

open testSim
sim testSim