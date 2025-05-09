function [ordine_scarto_out,ordine_scarto_vecchio,Cd_spe] = cdspe(scarto,ordine_scarto,Ec,Ed_corr,denom)

%int_inizio e int_fine presi da Felix da controllare cosa siano
int_inizio = 300; 
int_fine = 460; 

%  passo 1: filtro passa basso
T = length(Ec);
lung = 10;
Haar = [1/2,1/2];
ordine_scarto_vecchio = ordine_scarto;
ordine_scarto = conv(ordine_scarto,Haar,"same");
% scarto = conv(scarto,Haar,"same");

% passo 2: confronto con l'errore medio

e = 0;
param_1 = 0; 
param_3 = 1.5; % rateo per soglia superiore dell'errore da considerare rispetto all'errore medio
param_4 = 1; % rateo moltiplicato che va a moltiplicarsi per la media che detraggo

for j = 1:T-1    
    
    % determino media ordine_scarto
    if j <= lung
        media = mean(abs(ordine_scarto(j:j+lung))); 
    elseif j>lung && j<=2*lung
        media = mean(abs(ordine_scarto(j-e:j+lung)));
        e = e+1;
    elseif j >= T-1-lung
        media = mean(abs(ordine_scarto(j-lung:T-1)));
    else
        media = mean(abs(ordine_scarto(j-lung:j+lung)));
    end
    
    % verifico se entro la media
    if abs(scarto(j)) < param_4*media*Ec(j+1)
        scarto(j) = param_1*scarto(j); 
    elseif abs(scarto(j)) >= param_4*media*Ec(j+1) && abs(scarto(j)) < param_3*media*Ec(j+1)
        scarto(j) = scarto(j) - sign(scarto(j))*param_4*media*Ec(j+1); 
    else
        scarto(j) = sign(scarto(j))*param_3*media*Ec(j+1) - sign(scarto(j))*param_4*media*Ec(j+1); 
    end
end

Cd_spe = zeros(1,T-1);
for j=1:T-1
    Cd_spe(j) = (scarto(j)+Ed_corr(j))/(denom(j));
end

% passo 3: media mobile (moving average)
lung = 10; 

Cd_spe_reg = zeros(1,int_fine-int_inizio+1);
lambda = 0.9;
h = zeros(1,lung);

h(1) = 1-lambda;
for k=1:lung-1
        h(1+k) = lambda^k*h(1);
end
  
for n=1:int_fine-int_inizio+1
    
    j = 1;
    while (j<=lung-1 && int_inizio+n-j < size(Cd_spe,2)) 
        Cd_spe_reg(n) = Cd_spe_reg(n) + h(j)*Cd_spe(int_inizio+n-j);
        j = j+1;
    end
      
end
    
 ordine_scarto_out = ordine_scarto;

end

