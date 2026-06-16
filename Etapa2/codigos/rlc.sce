// Simulação Circuito RLC - Etapa 2
clear; clc;

// 1. Definição dos Parâmetros
L = 1.0;    // Indutância (H)
C = 0.1;    // Capacitância (F)
R = 2.0;    // Resistência (Ohms) - Altere este valor para ver o amortecimento

s = poly(0, 's');
num = 1;
den = L*C*s^2 + R*C*s + 1;
G = syslin('c', num / den);

// 2. Análise de Polos
polos = roots(den);
disp("Os polos do sistema são:");
disp(polos);

// 3. Resposta ao Degrau
t = 0:0.1:20;
y = csim('step', t, G);

// 4. Plotagem
clf();
plot(t, y, 'LineWidth', 2);
xtitle("Resposta ao Degrau - Circuito RLC", "Tempo (s)", "Tensão no Capacitor Vc(t)");
xgrid();
