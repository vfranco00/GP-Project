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
* **Função:** Desacoplar os produtores (carros
