

Rpm = BM19SundayPMAndrea.VarName6(:);
minimum = 100;
for i = 1:size(Rpm,1)-1
    if Rpm(i) > Rpm(i + 1)
        hypMin = (Rpm(i) - Rpm(i+1))/Rpm(i);
        if hypMin < minimum
            minimum = hypMin;
            istar = i;
        end
    end
end
minimum
istar
plot(1:320,Rpm);