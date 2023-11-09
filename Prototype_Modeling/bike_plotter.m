function bike_plotter(vel_lin_bo_RPM, vel_lin_corr, dist, vel_lin,power)

    yyaxis left
    plot(dist ,vel_lin_bo_RPM, dist, vel_lin_corr,dist, vel_lin);
    yyaxis right
    plot(dist,power);
    legend("vel lin bo RPM [Km/h]", "vel lin corr [Km/h]", "vel lin [Km/h]", "Power [W]");
    xlabel("Distance [Km]");
    title("Velocity Graph and Power");
    grid on 
    grid minor
    yyaxis right
    ylabel("Power [W]")
    yyaxis left
    ylabel("Velocity [Km/h]")

end