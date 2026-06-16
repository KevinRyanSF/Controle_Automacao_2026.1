// 1. Definindo a variável de Laplace e o vetor de tempo
s = %s;
t = 0:0.01:8;

// 2. Planta Genérica de 2ª Ordem (ex: dinâmica de um motor)
G = syslin('c', 1 / (s^2 + 3*s + 2));

// 3. Controle Proporcional (P)
Kp = 15;
C_p = Kp;
MalhaFechada_P = G*C_p / (1 + G*C_p);
y_p = csim('step', t, MalhaFechada_P);

// 4. Controle Proporcional-Integral (PI)
Ki = 15;
C_pi = Kp + Ki/s;
MalhaFechada_PI = G*C_pi / (1 + G*C_pi);
y_pi = csim('step', t, MalhaFechada_PI);

// 5. Controle Proporcional-Integral-Derivativo (PID)
Kd = 2;
C_pid = Kp + Ki/s + Kd*s; 
MalhaFechada_PID = G*C_pid / (1 + G*C_pid);
y_pid = csim('step', t, MalhaFechada_PID);

// 6. Plotando os resultados comparativos
clf();
plot(t, y_p, 'r', t, y_pi, 'b', t, y_pid, 'g');
xgrid(1);
legend(['Controle P (Erro em regime)', 'Controle PI (Zera erro, mais oscilatório)', 'Controle PID (Rápido e amortecido)'], 4);
xtitle('Resposta ao Degrau: Efeito das Acoes P, I e D', 'Tempo (s)', 'Amplitude');
