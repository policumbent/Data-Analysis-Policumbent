% This function gets the input angular velocity and gives the angular velocity of the wheel as an output 
% u_in : the angular velocity of the pedals (RPM)
% n : number of the middle gear teeth
% v : the angular velocity of the wheel (RPM)
% RPM : the column of datas from the pedal
function [torq, RPM_wheel_to_RPM_pedal, N ] = GearChangeDetect(RPM,power)
T = 1;
L = size(RPM,1);
N = ones(L,1);
RPM_wheel_to_RPM_pedal = ones(L,1);

for i=2:L-2
     if RPM(i+1) < RPM(i) && RPM(i+2) >= RPM(i+1) && RPM(i+3) >= RPM(i+2)
        N(i) = N(i-1)+1;
     else 
        N(i) = N(i-1);
     end
     n = N(i);
     u_in = RPM(i);

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
            
        v = u_in.*(108./T)*(38/18);

     end

    RPM_wheel_to_RPM_pedal(i) = v;
    torq = power./RPM;
    
end