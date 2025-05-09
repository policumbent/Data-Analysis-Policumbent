% This function gets the input angular velocity and gives the angular velocity of the wheel as an output 
% u_in : the angular velocity of the pedals (RPM)
% N : number of the middle gear teeth
% v : the angular velocity of the wheel (RPM)
% RPM : the column of datas from the pedal
% c :if c == 1 we assume constant RPM ın between gear changes
function [RPM_wheel_to_RPM_pedal, N ,vel_lin_bo_RPM] = GearChangeDetect(RPM)
T = 1;
L = size(RPM,1);
N = ones(L,1);
RPM_wheel_to_RPM_pedal = ones(L,1);
radius = 0.23157;

for i=2:L-2
     if RPM(i) < (RPM(i-1)*0.95) && RPM(i+2) >= RPM(i+1)
        N(i) = N(i-1)+1;
     else 
        N(i) = N(i-1);
     end
     n = N(i);
            
     for j = 1:length(n)
        if n == 12 
            T = 12;
            elseif n == 11
            T = 13;
            elseif n == 10
            T = 14;
            elseif n == 9
            T = 15;
            elseif n == 8
            T = 17;
            elseif n == 7
            T = 19;
            elseif n == 6
            T = 21;
            elseif n == 5
            T = 24;
            elseif n == 4
            T = 27;
            elseif n == 3
            T = 31;
            elseif n == 2
            T = 35;
            elseif n == 1
            T = 40;
        else 
            T = 12;
        end
     end

    v = u_in.*(108./T)*(38/18);

    RPM_wheel_to_RPM_pedal(i) = v;
    
end
vel_lin_bo_RPM = RPM_wheel_bo_RPM_pedal * radius * (pi/30) * 3.6; 
end
    