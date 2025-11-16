# RELATÓRIO TÉCNICO: SISTEMA DE MONITORAMENTO DISTRIBUÍDO (GP F1 BRASIL)

## 1. Visão Geral do Projeto
Este projeto consiste no desenvolvimento de um sistema distribuído para o monitoramento em tempo real da telemetria de pneus dos carros de Fórmula 1 durante o Grande Prêmio de Interlagos. O sistema foi projetado para suportar alta concorrência, utilizando uma arquitetura de microsserviços orquestrada via Docker.

## 2. Arquitetura do Sistema
O sistema segue uma arquitetura distribuída híbrida, implementando os três modelos de comunicação exigidos:

1.  **Baseada em Eventos (Pub/Sub):** Utilizada entre os Carros (Publicadores) e a Infraestrutura de Coleta (ISCCP) através de um Message Broker (RabbitMQ).
2.  **Baseada em Objetos:** Utilizada entre a Infraestrutura de Coleta (ISCCP) e os Servidores de Armazenamento (SSACP) via chamadas HTTP (API REST) enviando objetos JSON.
3.  **Baseada em Recursos:** Utilizada entre o Dashboard (Frontend) e o Servidor de Visualização (SSVCP) para consulta de dados persistidos.

## 3. Especificações Técnicas dos Componentes

### A. Subsistema de Coleta (SCCP) - "Carros"
* **Quantidade:** 24 instâncias (containers).
* **Função:** Simulam a geração de dados de telemetria (temperatura e pressão dos 4 pneus) e publicam mensagens em uma fila de eventos.
* **Tecnologia:** Python script com biblioteca `pika`.
* **Protocolo:** AMQP (Advanced Message Queuing Protocol).

### B. Message Broker
* **Tecnologia:** RabbitMQ (Imagem `rabbitmq:3-management`).
* **Função:** Desacoplar os produtores (carros) dos consumidores, garantindo que picos de dados não derrubem o sistema de processamento.

### C. Infraestrutura de Coleta (ISCCP)
* **Quantidade:** 15 instâncias (containers).
* **Função:** Atuam como consumidores da fila. Cada instância retira uma mensagem, processa (adiciona assinatura de rastreabilidade) e a envia para armazenamento.
* **Balanceamento:** Distribuição aleatória da carga para os nós de armazenamento.

### D. Subsistema de Armazenamento (SACP)
* **Componente SSACP:** 3 instâncias de servidores API (FastAPI). Recebem os objetos JSON e persistem no banco de dados.
* **Banco de Dados:** Cluster MongoDB com 3 nós (Replica Set `rs0`). Garante alta disponibilidade e tolerância a falhas.

### E. Subsistema de Visualização (SVCP)
* **Componente SSVCP:** API de Leitura (FastAPI) que consulta o banco de dados distribuído e expõe endpoints REST.
* **Dashboard:** Aplicação Web (React.js) que consome a API e exibe os dados em tempo real para as equipes.

## 4. Implementação e Tecnologias

| Tecnologia | Aplicação no Projeto |
| :--- | :--- |
| **Python 3.9** | Linguagem base para todos os microsserviços de backend. |
| **FastAPI** | Framework para criação das APIs REST (SSACP e SSVCP). |
| **Docker Compose** | Orquestração de 46 containers simultâneos. |
| **MongoDB** | Banco de dados NoSQL configurado em Cluster (Replica Set). |
| **RabbitMQ** | Gerenciamento de filas de mensagens assíncronas. |
| **React** | Interface de usuário responsiva e dinâmica. |

## 5. Instruções de Execução

O ambiente foi automatizado através de um script gerador de infraestrutura, devido à alta complexidade do arquivo `docker-compose.yml`.

**Passo 1: Geração da Infraestrutura**
Executar o script `generate_compose.py` para criar as definições dos 46 serviços e o script de inicialização do cluster de banco de dados.

**Passo 2: Inicialização**
Comando: `docker compose up -d --build`

**Passo 3: Acesso**
* **Dashboard:** http://localhost:3000
* **Monitoramento de Filas:** http://localhost:15672

## 6. Conclusão
O sistema atende a todos os requisitos funcionais e não-funcionais propostos, demonstrando a viabilidade de uma arquitetura distribuída escalável para cenários de telemetria crítica. A utilização de contêineres permitiu simular um ambiente complexo de produção em uma única máquina local.
