import json
import time
import random
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def simulate_event():
    return {
        "user_id": random.randint(1, 1000),
        "event_type": random.choice(["login", "logout", "purchase", "view"]),
        "timestamp": int(time.time()),
        "value": round(random.uniform(10.0, 500.0), 2) if random.random() > 0.5 else 0.0
    }

def main():
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'user_events'

    print("Starting Kafka producer...")
    try:
        while True:
            event = simulate_event()
            producer.produce(
                topic,
                key=str(event["user_id"]),
                value=json.dumps(event),
                callback=delivery_report
            )
            producer.poll(0)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()

if __name__ == "__main__":
    main()
