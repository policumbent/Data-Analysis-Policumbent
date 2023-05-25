function [fitresult, gof] = gearFit(dist, RPM_wheel_bo_RPM_pedal)
%% Fit: 'Wheel velocity'.
[xData, yData] = prepareCurveData( dist, RPM_wheel_bo_RPM_pedal );

% Set up fittype and options.
ft = fittype( 'exp2' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.Normalize = 'on';
opts.Robust = 'Bisquare';
opts.StartPoint = [2793.39441851214;-0.161015411051406;-1201.18884687413;-0.667177938883837];

% Fit model to data.
[fitresult, gof] = fit( xData, yData, ft, opts );
