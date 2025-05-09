function Lambda = dissFactorCalcCer(RPM_wheel_bo_RPM_pedal,vel_lin_bo_RPM,m,ID)

    [~,vel_lin,~,dist,~,~] = readRaceCer(ID);
    
    % Variables pre-allocation
    L = size(RPM_wheel_bo_RPM_pedal,1)-1;
    Jp = zeros(L);          % Energy calculated from linear velocity of the bike
    Jt = zeros(L);          % Energy calculated from RPM of the wheel
    delta_x = zeros(L);     % Difference between two subsequent data [Km]
    Ker_p = zeros(L);       % Rotational kinetic energy calculated from data
    Ker_t = zeros(L);       % Rotational kinetic energy calculated from RPM of the wheel
    I = 0.044;              % Inertia of the wheel
    radius = 0.23157;
    wheels = 3;

    for i = 2:L
        Jp(i) = 0.5 * m *(vel_lin(i)^2 + vel_lin(i-1)^2)/2;
        Jt(i) = 0.5 * m * (vel_lin_bo_RPM(i)^2 + vel_lin_bo_RPM(i-1)^2)/2;
        Ker_p(i) = 0.5 * I * wheels * ((vel_lin(i) / radius)^2 + (vel_lin(i-1) / radius)^2)/2;
        Ker_t(i) = 0.5 * I * wheels* ((vel_lin_bo_RPM(i) / radius)^2 + (vel_lin_bo_RPM(i-1) / radius)^2)/2;
        delta_x(i) = dist(i) - dist(i-1);
    end

    int_t = sum(Jt*delta_x') + sum(Ker_t*delta_x');
    int_p = sum(Jp*delta_x') + sum(Ker_p*delta_x');

    Lambda = int_p/int_t;    % Aka Dissipation Factor

end