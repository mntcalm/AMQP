import pika

def callback(ch, method, properties, body):
    print(f"Received {body}")
    # Здесь можно добавить обработку сообщения
    ch.basic_ack(delivery_tag = method.delivery_tag)

# Подключаемся к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Подписываемся на очередь
channel.queue_declare(queue='ram_queue', durable=True)

# Получаем сообщения из очереди 'ram_queue'
channel.basic_consume(queue='ram_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
