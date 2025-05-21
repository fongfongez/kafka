from confluent_kafka import Consumer, KafkaException
import sys

# 基本參數
KAFKA_BROKER_URL = '3.133.129.65:9092'  # Kafka broker
WORKSHOP_ID = 'tjr101'  # 與 Producer 相同
GROUP_ID = 'group10'  # Consumer group ID，可自行命名
TOPIC_NAME = WORKSHOP_ID.lower() + ".test"

# 設定 Consumer 參數
conf = {
    'bootstrap.servers': KAFKA_BROKER_URL,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',  # 從最早的訊息開始接收
}

# 建立 Kafka Consumer
consumer = Consumer(conf)

# 訂閱 topic
consumer.subscribe([TOPIC_NAME])

print(f"Listening to topic: {TOPIC_NAME} ...")

try:
    while True:
        msg = consumer.poll(1.0)  # 每 1 秒檢查一次有無新訊息

        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        # 印出收到的訊息
        key = msg.key().decode('utf-8') if msg.key() else None
        value = msg.value().decode('utf-8')
        print(f'Received message: key={key}, value={value}')

except KeyboardInterrupt:
    print("Consumer stopped by user.")

finally:
    # 關閉 consumer
    consumer.close()
