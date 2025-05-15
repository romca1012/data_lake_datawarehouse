from kafka import KafkaProducer
import json
from datetime import datetime
import uuid

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Exemple simple de transaction
message = {
    "transaction_id": str(uuid.uuid4()),
    "timestamp": datetime.now().isoformat(),
    "user_id": "U001",
    "user_name": "John Doe",
    "product_id": "P123",
    "amount": 299.99,
    "currency": "USD",
    "transaction_type": "purchase",
    "status": "completed",
    "location": {"city": "Paris", "country": "France"},
    "payment_method": "credit_card",
    "product_category": "electronics",
    "quantity": 1,
    "shipping_address": {"street": "123 Main St", "zip": "75000", "city": "Paris", "country": "France"},
    "device_info": {"os": "Windows", "browser": "Chrome", "ip_address": "192.168.1.1"},
    "customer_rating": 5,
    "discount_code": "SPRING10",
    "tax_amount": 20.0,
    "thread": 1,
    "message_number": 1,
    "timestamp_of_reception_log": datetime.now().isoformat()
}

producer.send('transaction_log', value=message)
producer.flush()
print(" Message envoyé dans Kafka -> transaction_log")