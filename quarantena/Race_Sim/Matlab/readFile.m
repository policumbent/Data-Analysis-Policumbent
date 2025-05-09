function [temp,umid,press,ws,wd,m,tyre,radius,ID] = readFile(IdRun)

table = readcell("ridecond.csv");
name = table(1:end,1);
table_size = size(table);
row = table_size(1);

for i=1:(row-1)
if strcmp(string(IdRun),(name(i,1)))==1
    temp = cell2mat(table(i,2));
    press = cell2mat(table(i,3));
    umid =  cell2mat(table(i,4));
    ws = cell2mat(table(i,5));
    wd = cell2mat(table(i,6));
    tyre = cell2mat(table(i,9));
        if strcmp(string(cell2mat(table(i,7))),'Andrea')
            m=92;
        elseif strcmp(string(cell2mat(table(i,7))),'Vittoria')
            m=80;
        end
        if cell2mat(table(i,9)) == 'Michelin'
            radius = 0.23157; % Michelin Blue 8 bar (20')
        elseif cell2mat(table(i,9)) == 'Continental'
            radius = 0.2291831; % Conti LTD 7 bar (20')
        end
end
i = i+1;
end
ID=append(IdRun,'.csv');
end