import json
import os
from kafka import KafkaConsumer

def consume_feeds(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    for feed in config['feeds']:
        consumer = KafkaConsumer(
            feed['topic'],
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        for message in consumer:
            data = message.value

if __name__ == "__main__":
    consume_feeds('config.json')