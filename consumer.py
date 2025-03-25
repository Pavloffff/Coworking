from kafka import KafkaConsumer

# Имя топика, из которого будем получать сообщения
topic = "test-topic"

# Инициализируем консюмера
consumer = KafkaConsumer(
    topic,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',  # Читаем сообщения с начала, если группа новая
    group_id='test-group'          # Назначаем имя группы консюмеров
)

print("Ожидание сообщений...")
for message in consumer:
    print(f"Получено: {message.value.decode('utf-8')}")
