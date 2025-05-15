from kafka import KafkaConsumer
import json
import os
from datetime import datetime
import traceback

KAFKA_TOPIC = "transaction_log"
BOOTSTRAP_SERVERS = "localhost:9092"
DATA_LAKE_PATH = "data_lake/all_transactions"

def main():
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='datalake-consumer-group',
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

        print("Kafka Consumer connecté. En attente de messages...")

        for message in consumer:
            try:
                record = message.value
                date = datetime.now().strftime("%Y-%m-%d")
                partition_path = os.path.join(DATA_LAKE_PATH, date)
                os.makedirs(partition_path, exist_ok=True)

                filename = os.path.join(partition_path, "batch.json")
                with open(filename, "a") as f:
                    json.dump(record, f)
                    f.write("\n")

                print(f"Message écrit dans : {filename}")

            except Exception as e:
                print("Erreur lors de l écriture d un message dans le fichier.")
                traceback.print_exc()

    except Exception as e:
        print("Erreur de connexion à Kafka ou autre erreur générale :")
        traceback.print_exc()

if __name__ == "__main__":
    main()
