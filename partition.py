from kafka import KafkaConsumer
import json
import os
from datetime import datetime

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

def consume_data():
    consumer = KafkaConsumer(
        'transaction_log',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='consumer-group-1',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        data = message.value
        date_str = datetime.now().strftime("%Y-%m")
        file_path = f"Data_lake/{date_str}/transactions.json"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)


        with open(file_path, 'a') as f:
            json.dump(data, f)
            f.write('\n')

if __name__ == "__main__":
    consume_data()