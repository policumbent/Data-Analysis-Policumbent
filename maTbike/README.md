# __Modello Simulink__

## Obiettivo

Creare un modello fisico della bici in simulink che descriva il suo comportamento durante la marcia partendo dal vecchio modello e migliorandone l'accuratezza

## Cose da Fare

- implementare funzione per il calcolo della densità dell'aria in funzione dell'altitudine e della temperatura

    - prendere i dati relativi all'altitudine dal gps e e metterli in input per avere in output il valore della densità dell'aria sempre aggiornato 

    - $${git \displaystyle \rho _{z}={\frac {P_{z}}{RT_{z}}}=\rho _{0}\left(1+{\frac {\lambda z}{T_{0}}}\right)^{-\left(1+{\frac {g}{R\lambda }}\right)}}$$ : equazione per il calcolo della densità dell'aria utilizzata dall' ICAO


    - $ \lambda = -0,0065 \frac{K}{m} $ :   gradiente termico verticale


    - $ R = 287,05287 \ \frac{J}{kgK}$


    - $ g = 9,80665 \ \frac{m}{s^2}$

    - $ \rho_0 = 1,225 \ \frac{kg}{m^3} $ densità aria misurata in condizioni standard

    - $ T_0 = 288,15 \ K $ temperatura in condizioni standard

- aggiornare il calcolo dell'accelerazione passando da approssimare la ruota da un punto materiale ad un corpo rigido 

    - $ a = \frac{C \ d}{2I \ + \frac{m \ D^2}{2}}$
    
    - C : coppia che viene trasmessa alla ruota 
    - d : diametro medio ruota
    - $ I $ : momento d'inerzia ruota
    - m : massa ruota


- aggiornare il calcolo della della rolling restitence 
    
    - ricerca dei coefficienti di attrito volevente 

    - rircerca influenza della temperatura sui coefficienti di attrito volvente 

    - calcolo della forza agente sulla ruota considerando la posizione del centro di massa del veicolo rispetto alla ruota aggiungendo un bilancio di momenti

    - ricercare aziende/laboratori che potrebbero effettuare dei test sugli pneumatici e farli contattare da gestione per convicergli a farlo in cambio di un logo e una stretta di mano

        - **PontLab** : laboratorio di ricerca sui materiali 
        - **Pirelli** : bello ma ahahhaha; ha collaborato con team come Trek-Segafredo e AG2R Citroën, dimostrando interesse per progetti innovativi nel settore ciclistico
        - **TestIndustry** : produce banchi proca, magari ce ne fa usare uno o ce lo regala 
        - **ToProveLab**
        - **Vittoria s.p.a** azienda molto figa che produce pneumatici ad alte prestazioni e **costosi** solo per bici, ho dato un occhiata e hanno cose molto interessanti se si decidesse di adottare nuove soluzioni 

- capire insieme agli aerodinamici a quali velocità sono più apprezzabili le variazioni di $ C_x $ poichè, a detta loro, le analisi cfd per il calcolo di questi ultimi sono molto lunghe e non possono essere fatte per tutte le velocità

- aggiungere perdite meccaniche non considerate in precedenza 

- capire se fattibile studiare il rendimento del cambio adattando il banco prova già esistente 
 

  
