function [temp,humid,press,ws,wd,m,tyre,radius,ID] = readCond(IdRun)

% Just common table initializations
table = readcell("ridecond.csv");
name = table(1:end,1);
table_size = size(table);
row = table_size(1);

% Assigns table columns to variables
for i=1:(row-1)
    if strcmp(string(IdRun),(name(i,1))) == 1  
        temp = cell2mat(table(i,2));            % Temperature of the race field 
        press = cell2mat(table(i,3));           % Pressure of the race field
        humid = cell2mat(table(i,4));           % Humidity, percentage
        ws = cell2mat(table(i,5));              % Wind speed
        wd = cell2mat(table(i,6));              % Wind direction (respect : north)
        tyre = cell2mat(table(i,9));

% Compares name of the driver and assigns the mass (m = driver + bike)
        if strcmp(string(cell2mat(table(i,7))),'Andrea')
            m = 92;
        elseif strcmp(string(cell2mat(table(i,7))),'Vittoria')
            m = 80;
        end

% Compares the tyre and assigns the radius
        if cell2mat(table(i,9)) == 'Michelin'
            radius = 0.23157;               % Michelin Blue 8 bar (20')
        elseif cell2mat(table(i,9)) == 'Continental'
            radius = 0.2291831;             % Conti LTD 7 bar (20')
        end
    end
i = i+1;
end

% Joins the IdRun and the extension .csv, useful with the other functions
ID = append(IdRun,'.csv');
end