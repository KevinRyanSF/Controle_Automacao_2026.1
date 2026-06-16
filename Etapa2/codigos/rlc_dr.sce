// Variação da Resistência R no Circuito RLC
clear; clc; clf();
L = 1.0; 
C = 0.1;
R_vals = [0.5, 2.0, 6.32, 12.0]; 

t = 0:0.1:30;
s = poly(0, 's');

colors = ['r', 'g', 'b', 'k'];
legends = [];

for i = 1:length(R_vals)
    R = R_vals(i);
    den = L*C*s^2 + R*C*s + 1;
    G = syslin('c', 1 / den);
    y = csim('step', t, G);
    
    plot(t, y, colors(i), 'LineWidth', 2);
    legends($+1) = 'R = ' + string(R) + ' Ohms';
    
    disp("Polos para R = " + string(R) + ":");
    disp(roots(den));
end

xtitle("Efeito da Variacao da Resistencia no Circuito RLC", "Tempo (s)", "Tensao Vc(t)");
legend(legends, 'in_lower_right');
xgrid();
