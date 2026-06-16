# Projeto Integrador Final: Gêmeo Digital e Controle PID da Mesa Labirinto

[![Apresentação no YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/inMYiDDdv4s)

## Objetivo
Coroar a disciplina de Controle e Automação I aplicando a teoria de sistemas dinâmicos em um desafio prático de engenharia. O projeto consiste na modelagem matemática, sintonia de controle em malha fechada e desenvolvimento de um Gêmeo Digital interativo para o rastreamento de trajetória em uma plataforma de equilíbrio bi-dimensional (Mesa Labirinto).

## Estrutura do Diretório
- `/documentos`: Relatório técnico completo detalhando as equações da mecânica, análise de estabilidade e a síntese do controlador digital.
- `/imagens`: Gráficos de simulação e capturas da interface de telemetria.
- `/simulador`: Código-fonte do Gêmeo Digital em Python e malha 3D do labirinto exportada do ambiente CAD.

## Arquitetura do Sistema e Engenharia
O projeto foi estruturado em três pilares fundamentais:

1. **Modelagem Mecânica e Controle:**
   - Obtenção da planta (duplo integrador) a partir da Segunda Lei de Newton.
   - Síntese do Controlador PID para fornecer amortecimento e zerar erros de regime no rastreamento contínuo.
   - Implementação de segurança de hardware via anti-windup e saturação rigorosa dos servomotores, limitados a atuar num range máximo de 90 graus totais.

2. **Gêmeo Digital (Digital Twin):**
   - Motor de física customizado com sub-stepping para garantir colisões precisas.
   - Paradigma Human-in-the-Loop (HITL) permitindo o controle de setpoint e navegação 3D utilizando um gamepad.

3. **Supervisório SCADA e IHM:**
   - Interface em split-screen com um painel de telemetria dedicado.
   - Gráficos de alta resolução estilo osciloscópio comparando a curva do ângulo alvo versus o real em tempo real.
   - Minimapa histórico projetado ortogonalmente mantendo um raio físico fixo em metros, garantindo precisão métrica da localização do dispositivo.

## Como Executar o Simulador
1. Certifique-se de ter o Python 3 instalado juntamente com a biblioteca `ursina` (`pip install ursina`).
2. Conecte um gamepad compatível ao computador.
3. Navegue até a pasta `/simulador` e execute o arquivo principal:
   ```bash
   python mesa_labirinto.py
4. Utilize o Analógico Esquerdo para inclinar a plataforma e os Gatilhos/Analógico Direito para gerenciar a câmera e acompanhar a telemetria do PID.