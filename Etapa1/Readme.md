# Etapa 1: Fundamentos Teóricos - Sistemas Dinâmicos

Este diretório contém a primeira etapa do Estudo Dirigido de Controle e Automação I, focada na construção da base teórica sobre sistemas dinâmicos.

## 1. Resumo Teórico

### Transformada de Laplace e Função de Transferência
A Transformada de Laplace converte equações diferenciais no domínio do tempo em equações algébricas no domínio da frequência complexa s (s = σ + jω). A Função de Transferência (FT) é a razão entre a saída Y(s) e a entrada U(s) de um sistema linear invariante no tempo, considerando condições iniciais nulas:

G(s) = Y(s) / U(s)

### Polos e Zeros
* **Polos:** São as raízes do polinômio do denominador. Eles determinam os modos naturais de resposta do sistema e apontam as frequências onde a função de transferência tende ao infinito.
* **Zeros:** São as raízes do polinômio do numerador, representando as frequências onde a saída do sistema se anula.

### Análise de Estabilidade
A estabilidade do sistema é avaliada pela localização de seus polos no plano complexo:

| Localização dos Polos | Parte Real (σ) | Comportamento do Sistema | Estabilidade |
| :--- | :--- | :--- | :--- |
| Semiplano Esquerdo | σ < 0 | Resposta decai exponencialmente com o tempo. | Estável |
| Eixo Imaginário | σ = 0 | Oscilações sustentadas (não decaem nem crescem). | Marginalmente Estável |
| Semiplano Direito | σ > 0 | Resposta cresce exponencialmente. | Instável |

### Resposta Temporal de Sistemas de Segunda Ordem
A forma canônica de um sistema de segunda ordem possui uma frequência natural não-amortecida e um fator de amortecimento (ζ). O comportamento transiente é classificado por ζ:

* ζ > 1 (Superamortecido): Polos reais e negativos distintos. Resposta não oscila e converge lentamente.
* ζ = 1 (Criticamente Amortecido): Polos reais, iguais e negativos. Resposta mais rápida sem apresentar oscilação (overshoot).
* 0 < ζ < 1 (Subamortecido): Polos complexos conjugados com parte real negativa. A resposta oscila com amplitude decrescente.
* ζ = 0 (Não Amortecido): Polos puramente imaginários. O sistema oscila indefinidamente.

## 2. Simulação Computacional
As simulações computacionais foram desenvolvidas na linguagem Scilab. O objetivo foi plotar e analisar a resposta ao degrau de funções de transferência de segunda ordem variando o fator de amortecimento ζ.

*(Consulte a pasta `/Codigos` para o script `.sce` e a pasta `/Imagens` para a visualização das curvas geradas).*

## 3. Discussão e Aplicações Reais
Os modelos matemáticos possuem uma correlação direta com os fenômenos físicos reais. Analisando um circuito RLC, por exemplo, nota-se que o fator de amortecimento do sistema está diretamente relacionado à resistência (que causa a dissipação de energia). Em paralelo, a frequência natural do circuito vincula-se ao indutor e ao capacitor, que são os elementos armazenadores de energia. 

Na automação industrial e em sistemas embarcados, projetar e ajustar corretamente a localização desses polos é o que garante a estabilidade no controle e no funcionamento seguro físico e eletromecânico do maquinário.
