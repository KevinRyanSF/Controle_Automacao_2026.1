# Etapa 2: Modelagem e Simulação - Circuito RLC em Série

## Objetivo
Realizar a modelagem matemática, a análise de estabilidade e a simulação computacional de um circuito RLC em série, avaliando a tensão sobre o capacitor. O estudo engloba a simulação analítica via script e a implementação numérica através de diagramas de blocos.

## Estrutura do Diretório
- `/documentos`: Relatório técnico em PDF contendo todo o equacionamento e análises detalhadas, além do código-fonte em LaTeX.
- `/imagens`: Gráficos de resposta ao degrau e o diagrama de blocos implementado.
- `/codigos`: 
  - Script em Scilab (`.sce`) para cálculo de polos e plotagem analítica.
  - Diagrama de blocos do Xcos (`.zcos`) para simulação numérica.

## Modelagem Matemática
A Função de Transferência do sistema no domínio de Laplace, que relaciona a tensão de saída no capacitor $V_c(s)$ com a tensão de entrada $V_i(s)$, foi deduzida como:

$$G(s) = \frac{1}{LCs^2 + RCs + 1}$$

## Principais Conclusões
* **Análise de Polos e Estabilidade:** Com os parâmetros iniciais ($L = 1.0$ H, $C = 0.1$ F, $R = 2.0$ $\Omega$), os polos resultaram em $s_{1,2} = -1 \pm 3j$. A parte real estritamente negativa comprova a estabilidade do sistema, apresentando uma resposta transitória subamortecida.
* **Validação Numérica:** A implementação da equação diferencial no Xcos com integradores em cascata produziu resultados idênticos à simulação da Função de Transferência, validando o modelo.
* **Efeito do Amortecimento:** A variação do resistor $R$ demonstrou de forma clara a transição do sistema entre os regimes subamortecido, criticamente amortecido (estabilização ideal) e superamortecido (resposta lenta).

## Como Executar
1. Abra o software Scilab.
2. Para a análise analítica, execute o script `.sce` localizado na pasta `/codigos`.
3. Para a simulação em blocos, abra o ambiente Xcos e carregue o arquivo `.zcos`. Execute a simulação para visualizar a resposta no osciloscópio numérico.