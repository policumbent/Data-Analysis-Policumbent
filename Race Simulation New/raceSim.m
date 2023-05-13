clc
clear all
close all

%% Data inquiry 

[temp,humid,press,ws,wd,m,tyre,radius,ID] = readCond('BM_19_Tuesday_AM_Andrea');

[time,torq,vel,power,dist,RPM,Hrate,Alt] = readRace(ID);

%% Gear Effect

L = size(RPM,1);
n = ones(L,1);
v = ones(L,1);

for i = 2:L-2
    if RPM(i+1) < RPM(i) && RPM(i+2) < RPM(i+1) || RPM(i) > RPM(i+1)*1.1  
        n(i) = n(i-1)+1 ;
    else 
        n(i) = n(i-1) ;
        
    end
    v(i) = gearchange(n(i),RPM(i));

end 

Alt = Alt-Alt(1);

%% Results and Plots 

vel_RPM = v*radius*pi/30*(3); 
error = mean(100*abs(vel-vel_RPM) ./vel);
velocityy = vel / radius *30/pi/3.6; 
%plot(time,vel,time,power,time,RPM,time,v,time,vel_RPM);
figure
plot(time,vel,time,power,time,RPM,time,v,time,vel_RPM,time,velocityy);
grid on
grid minor
legend('Velocity','Power','RPM','RPMwheel','velRPM','Velicity projected');
