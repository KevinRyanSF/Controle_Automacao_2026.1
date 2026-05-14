// Script Scilab - Análise de Sistemas de Segunda Ordem
wn = 10; // Frequencia natural em rad/s
zetas = [0.1, 0.4, 0.7, 1.0, 1.5]; // Diferentes amortecimentos

s = poly(0, 's'); // Define 's' como a variável complexa polinomial
scf(1); // Abre ou mantém a janela gráfica 1
clf(); // Limpa a figura para não sobrepor execuções anteriores
t = 0:0.01:2; // Vetor de tempo de 0 a 2 segundos
for i = 1:length(zetas)
z = zetas(i);
// 1. Definição da Função de Transferência no Scilab
num = wn^2;
den = s^2 + 2*z*wn*s + wn^2; // Monta o polinômio do denominador
G = syslin('c', num / den); // 'c' indica sistema contínuo no tempo
// 2. Extração e exibição dos polos no console
p = roots(den);
disp(['ζ = ' + string(z) + ' Polos:']);
disp(p);
// 3. Simulação da Resposta ao Degrau
y = csim('step', t, G);
// 4. Plotagem da curva
plot(t, y, 'LineWidth', 2);
end
// Formatação do Gráfico
legend(['z=0.1', 'z=0.4', 'z=0.7', 'z=1.0', 'z=1.5'], 'in_lower_right');
title('Resposta ao Degrau para Diferentes Fatores de Amortecimento');
xlabel('Tempo (s)');
ylabel('Amplitude');
xgrid;
