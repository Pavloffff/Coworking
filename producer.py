from kafka import KafkaProducer
import time

# Имя топика, в который будем отправлять сообщения
topic = "test-topic"

# Инициализируем продюсера, указываем адрес Kafka (localhost:9092)
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Отправим 10 тестовых сообщений
for i in range(10):
    message = f"Test message {i}"
    producer.send(topic, message.encode('utf-8'))
    print(f"Отправлено: {message}")
    time.sleep(1)

producer.flush()  # Дожидаемся отправки всех сообщений
producer.close()
