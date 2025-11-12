import pika
import time
import json
import os
import requests

rabbitmq_host = 'rabbitmq'
exchange_name = 'car_events_exchange'
binding_key = 'car.tires'
queue_name = 'isccp_tire_data_queue'

mongo_host = 'mongo'
mongo_port = 27017
mongo_db_name = 'gp_db'
mongo_collection_name = 'tire_data'

ssacp_url = 'http://ssacp_01:8000/tires'

isccp_id = os.getenv('ISCCP_ID', 'isccp_unknown')

def send_to_ssacp(data):
    try:
        response = requests.post(ssacp_url, json=data)
        if response.status_code == 200:
            print(f"[{isccp_id}] Dados enviados ao SSACP com sucesso.")
        else:
            print(f"[{isccp_id}] Falha ao enviar dados ao SSACP. Status Code: {response.status_code}")
    except Exception as e:
        print(f"[{isccp_id}] Erro ao enviar dados ao SSACP: {e}")


def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode('utf-8'))
        car_id = data.get('car_id', 'unknown')
        print(f"[{isccp_id}] < Evento recebido do Carro {car_id}")

        send_to_ssacp(data)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[{isccp_id}] Erro ao processar a mensagem: {e}")   
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    """ Inicia o consumidor RabbitMQ com retentativas. """
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

            print(f"[{isccp_id}] Conectado ao RabbitMQ. Esperando por eventos...")

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"[{isccp_id}] Erro de conexão com RabbitMQ: {e}. Tentando novamente em 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"[{isccp_id}] Erro inesperado no consumidor: {e}. Reiniciando em 10s...")
            time.sleep(10)

if __name__ == '__main__':
    start_consumer()