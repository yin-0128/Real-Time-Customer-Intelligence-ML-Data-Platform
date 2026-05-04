import json
from confluent_kafka import Consumer, KafkaError, KafkaException

def main():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'ingestion_group',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = Consumer(conf)
    topic = 'user_events'
    
    consumer.subscribe([topic])
    print(f"Subscribed to topic: {topic}")
    
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            
            val = msg.value().decode('utf-8')
            print(f"Received message: {val}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
