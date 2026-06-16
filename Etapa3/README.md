# Etapa 3: Controle em Malha Fechada e Controlador PID

## Objetivo
Estudar a teoria, a simulação e a implementação de controladores PID (Proporcional-Integral-Derivativo). Esta etapa abrange desde a análise no domínio da frequência contínua até a discretização do algoritmo para execução em sistemas embarcados, culminando na análise prática de saturação em uma plataforma mecatrônica.

## Estrutura do Diretório
- `/documentos`: Relatório técnico em PDF contendo o embasamento teórico, as equações de discretização e a análise crítica da aplicação.
- `/imagens`: Gráfico comparativo da resposta ao degrau para os controladores P, PI e PID.
- `/codigos`: Script em Scilab (`.sce`) utilizado para simular a malha de controle da planta de segunda ordem.

## Formalização Matemática
A função de transferência do controlador PID no domínio contínuo é dada por:

$$C(s) = K_p + \frac{K_i}{s} + K_d s$$

Para a implementação digital no microcontrolador, a lei de controle foi discretizada (utilizando Euler retangular e diferenças finitas), resultando na seguinte equação a cada período de amostragem $T_s$:

$$u[k] = K_p \cdot e[k] + I[k-1] + K_i \cdot T_s \cdot e[k] + K_d \cdot \frac{e[k] - e[k-1]}{T_s}$$

## Principais Conclusões
* **Simulação Analítica:** A ação Proporcional apresentou erro em regime permanente; a adição da Integral zerou o erro mas gerou sobressinal; por fim, a ação Derivativa atuou como um amortecedor, garantindo uma estabilização rápida e precisa da planta $G(s) = \frac{1}{s^2 + 3s + 2}$.
* **Desafios no Firmware:** A implementação de um PID digital exige tratamento cuidadoso do tempo de amostragem ($T_s$) e a utilização de filtros para atenuar o ruído inerente à derivada discreta.
* **Saturação e Anti-Windup:** Na aplicação prática da Mesa Labirinto operada pelo ESP32, é obrigatória a inclusão de uma trava física virtual. A lógica de *anti-windup* implementada impede que o esforço de controle force os servomotores além do limite operacional rigoroso de 90 graus totais, evitando travamentos mecânicos e garantindo a segurança estrutural do sistema.

## Como Executar
1. Abra o software Scilab.
2. Navegue até a pasta `/codigos` e abra o script `.sce`.
3. Execute o código para visualizar a geração dinâmica do gráfico de comparação (P vs PI vs PID).