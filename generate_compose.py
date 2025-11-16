# Arquivo: generate_compose.py
import os

# Configuração das Quantidades
NUM_CARS = 24
NUM_ISCCP = 15
NUM_SSACP = 3
NUM_MONGO = 3

# ---------------------------------------------------------
# PASSO 1: Criar o arquivo JS auxiliar para o Mongo
# Isso evita erros de aspas no terminal
# ---------------------------------------------------------
js_content = """
rs.initiate({
    _id: "rs0",
    members: [
        { _id: 0, host: "mongo1:27017" },
        { _id: 1, host: "mongo2:27017" },
        { _id: 2, host: "mongo3:27017" }
    ]
});
"""

with open("init_replica.js", "w") as f:
    f.write(js_content)
print("✅ Arquivo 'init_replica.js' criado com sucesso.")

# ---------------------------------------------------------
# PASSO 2: Gerar o Docker Compose
# ---------------------------------------------------------

docker_compose_content = f"""version: '3.8'

services:
  # ----------------------------------------------------
  # Infraestrutura Base
  # ----------------------------------------------------
  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "check_running"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - gp_network

  dashboard:
    build: ./dashboard_app
    container_name: gp_dashboard
    ports:
      - "3000:3000"
    environment:
      - WATCHPACK_POLLING=true
    volumes:
      - ./dashboard_app/src:/app/src
    networks:
      - gp_network

  # ----------------------------------------------------
  # Inicializador do Cluster Mongo (Agora via Arquivo)
  # ----------------------------------------------------
  mongo-init:
    image: mongo
    depends_on:
      - mongo1
      - mongo2
      - mongo3
    volumes:
      - ./init_replica.js:/init_replica.js
    command: >
      bash -c "sleep 15 && mongosh --host mongo1:27017 /init_replica.js"
    networks:
      - gp_network

  # ----------------------------------------------------
  # Cluster MongoDB (3 Nós)
  # ----------------------------------------------------
"""

# Gerar Mongos
mongo_hosts = []
for i in range(1, NUM_MONGO + 1):
    mongo_hosts.append(f"mongo{i}")
    docker_compose_content += f"""
  mongo{i}:
    image: mongo
    container_name: mongo{i}
    command: ["--replSet", "rs0", "--bind_ip_all"]
    ports:
      - "{27017 + i - 1}:27017"
    volumes:
      - mongo-data-{i}:/data/db
    networks:
      - gp_network
"""

# Gerar SSACP
for i in range(1, NUM_SSACP + 1):
    docker_compose_content += f"""
  ssacp_{i:02d}:
    build: ./ssacp_service
    container_name: ssacp_{i:02d}
    depends_on:
      - mongo1
      - mongo2
      - mongo3
    networks:
      - gp_network
"""

# Gerar SSVCP
docker_compose_content += f"""
  ssvcp_01:
    build: ./ssvcp_service
    container_name: ssvcp_01
    ports:
      - "8001:8001"
    depends_on:
      - mongo1
      - mongo2
      - mongo3
    networks:
      - gp_network
"""

# Gerar ISCCP
for i in range(1, NUM_ISCCP + 1):
    docker_compose_content += f"""
  isccp_{i:02d}:
    build: ./isccp_service
    container_name: isccp_{i:02d}
    environment:
      - ISCCP_ID=isccp-{i:02d}
      - PYTHONUNBUFFERED=1
    depends_on:
      rabbitmq:
        condition: service_healthy
    networks:
      - gp_network
"""

# Gerar Carros
for i in range(1, NUM_CARS + 1):
    docker_compose_content += f"""
  car_{i:02d}:
    build: ./car_simulator
    container_name: car_{i:02d}
    environment:
      - CAR_ID=car-{i:02d}
      - PYTHONUNBUFFERED=1
    depends_on:
      rabbitmq:
        condition: service_healthy
    networks:
      - gp_network
"""

# Finalização
docker_compose_content += """
networks:
  gp_network:
    driver: bridge

volumes:
"""
for i in range(1, NUM_MONGO + 1):
    docker_compose_content += f"  mongo-data-{i}:\n    driver: local\n"

with open("docker-compose.yml", "w") as f:
    f.write(docker_compose_content)

print("✅ docker-compose.yml gerado com sucesso!")