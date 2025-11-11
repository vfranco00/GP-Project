import pika
import time
import json
import os
from pymongo import MongoClient

rabbitmq_host = 'rabbitmq'
exchange_name = 'car_events_exchange'
binding_key = 'car.tires'
queue_name = 'isccp_tire_data_queue'

mongo_host = 'mongo'
mongo_port = 27017
mongo_db_name = 'gp_db'
mongo_collection_name = 'tire_data'

isccp_id = os.getenv('ISCCP_ID', 'isccp_unknown')

def connect_mongo():
    while True:
        try:
            client = MongoClient(host=mongo_host, port=mongo_port)
            client.admin.command('ping')
            print(f"[{isccp_id}] Conectado ao MongoDB (host: {mongo_host})")
            db = client[mongo_db_name]
            collection = db[mongo_collection_name]
            return client, collection
        except Exception as e:
            print(f"[{isccp_id}] Erro ao conectar ao MongoDB: {e}")
            time.sleep(5)

def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode('utf-8'))
        client, collection = connect_mongo()
        collection.insert_one(data)
        client.close()

        car_id = data.get('car_id', 'unknown_car')
        temp = data.get('tires', {}).get('front_left', {}).get('temp', 'N/A')

        print(f"[{isccp_id}] > Dados de pneus armazenados no MongoDB (Carro: {data['car_id']})")

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