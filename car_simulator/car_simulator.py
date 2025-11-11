import pika
import time
import random
import json
import os

car_id = os.getenv('CAR_ID', 'car_001')
rabbitmq_host = 'rabbitmq'
exchange_name = 'car_events_exchange'
routing_key = 'car.tires'

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbitmq_host)
            )
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
            
            print(f"[{car_id}] Conectado ao RabbitMQ (Exchange: {exchange_name})")
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ to be available...")
            time.sleep(5)

def generate_tire_data():
    return {
        'timestamp': time.time(),
        'car_id': car_id,
        'tires': {
            'front_left': {'temp': round(random.uniform(80, 110), 2), 'pressure': round(random.uniform(20, 25), 2), 'wear': round(random.uniform(0, 1), 2)},
            'front_right': {'temp': round(random.uniform(80, 110), 2), 'pressure': round(random.uniform(20, 25), 2), 'wear': round(random.uniform(0, 1), 2)},
            'rear_left': {'temp': round(random.uniform(80, 110), 2), 'pressure': round(random.uniform(20, 25), 2), 'wear': round(random.uniform(0, 1), 2)},
            'rear_right': {'temp': round(random.uniform(80, 110), 2), 'pressure': round(random.uniform(20, 25), 2), 'wear': round(random.uniform(0, 1), 2)},
        }
    }

connection, channel = connect_rabbitmq()

try:
    while True:
        sleep_time = random.uniform(5, 10) 
        time.sleep(sleep_time)
        
        data = generate_tire_data()
        message_body = json.dumps(data)
        
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message_body
        )
        
        print(f"[{car_id}] > Evento Publicado (Temp: {data['tires']['front_left']['temp']}°C)")

except KeyboardInterrupt:
    print(f"[{car_id}] Desligando...")
    connection.close()
except Exception as e:
    print(f"[{car_id}] Erro inesperado: {e}")
    if connection.is_open:
        connection.close()