clear all
close all
clc

%% Impostare pendenza da usare
% se pendenza = 1 (pendenza_nuova_media_viagg.csv);
% se pendenza = 0 (pendenza_migliorata.csv).

pendenza = 0;

%% Impostare giorno, ruote usate, se c'era vento, se era costante, l'angolo, la sua velocità e il rider

% Vento NO: vento = 0;
% Vento SI': vento = 1;
% Vento COSTANTE: cost = 1;
% Vento NON COSTANTE: cost = 0;
% Angolo vento: vettore angolo con angolo(1) = angolo iniziale; 
% angolo(2) = angolo finale;
% Se Vento con angolo costante angolo(2) = 0;

vento = 1;
cost = 1;
angolo = [0,45];

%% Simulazione
vel = velocitaSimulata(pendenza, vento, cost,'BM_19_Tuesday_AM_Andrea',angolo);
Vel = vel(1);
Vel;
