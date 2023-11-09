% This function gets the input angular velocity and gives the angular velocity of the wheel as an output 
% N : number of the middle gear teeth
% v : the angular velocity of the wheel (RPM)
% RPM : the column of datas from the pedal
function [RPM_wheel_bo_RPM_pedal, N ,vel_lin_bo_RPM] = GearChangeDetectCer(RPM)
T = 1;
L = size(RPM,1);
N = ones(L,1);
RPM_wheel_bo_RPM_pedal = ones(L,1);
radius = 0.23157;

for i=2:L-2

     if RPM(i) < (RPM(i-1)*0.95) && RPM(i-1) >= RPM(i-2)
        N(i) = N(i-1)+1;
     else 
        N(i) = N(i-1);
     end

     n = N(i);
            
     for j = 1:length(n)
        if n == 7
            T = 15;
            elseif n == 6
            T = 17;
            elseif n == 5
            T = 19;
            elseif n == 4
            T = 21;
            elseif n == 3
            T = 24;
            elseif n == 2
            T = 28;
            elseif n == 1
            T = 32;
        end
     end

    RPM_wheel_bo_RPM_pedal(i) = RPM(i)*(60/T)*(54/17);
end
vel_lin_bo_RPM = RPM_wheel_bo_RPM_pedal * radius * (pi/30) * 3.6; 
end