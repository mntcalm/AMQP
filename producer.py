# импортируем psutil  для извлечения параметров и pika - для общения по AMQP
import psutil
import pika

def get_temperature_data():
    # формируем словарь НазваниеДатчика:значениеТемпературы
    sensors = psutil.sensors_temperatures()
    temperature_data = {}
    for name, entries in sensors.items():
        for entry in entries:
            key = f"temperature.{entry.label or name}"
            temperature_data[key] = entry.current
    return temperature_data

def get_ram_data():
	# извлекаем: памяти всего и % использованой памяти
    # 
    ram = psutil.virtual_memory()
    ram_data = {
        "ram.total": ram.total,
        "ram.used_percent": ram.percent
    }
    return ram_data


# Настройка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Объявление обменника
channel.exchange_declare(exchange='telemetry_exchange', exchange_type='direct', durable=True)




# извлекаем температуры из функции, печатаем извлеченное
temperature_data = get_temperature_data()
for key, value in temperature_data.items():
    print(f"{key}: {value}")
	#print(key, " - ", value)
    channel.basic_publish(exchange='telemetry_exchange', routing_key=key, body=str(value))
	
	
	
# извлекаем и печатаем данные по RAM
ram_data = get_ram_data()
for key, value in ram_data.items():
    print(key, ":", value)
    channel.basic_publish(exchange='telemetry_exchange', routing_key=key, body=str(value))
	
	
# Закрытие соединения с обменником (RabbitMQ)
connection.close()
