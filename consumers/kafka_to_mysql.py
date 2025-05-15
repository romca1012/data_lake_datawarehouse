from kafka import KafkaConsumer
import json
import mysql.connector
import traceback

def main():
    consumer = KafkaConsumer(
        'transaction_log',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='warehouse-consumer-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="datawarehouse"
    )
    cursor = db.cursor()

    insert_query = """
    INSERT INTO all_transactions (
        transaction_id, timestamp, user_id, user_name, product_id, amount,
        currency, transaction_type, status, city, country, payment_method,
        product_category, quantity, shipping_street, shipping_zip,
        shipping_city, shipping_country, device_os, device_browser, device_ip,
        customer_rating, discount_code, tax_amount, thread, message_number,
        timestamp_of_reception_log
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for msg in consumer:
        try:
            r = msg.value
            values = (
                r["transaction_id"], r["timestamp"], r["user_id"], r["user_name"], r["product_id"],
                r["amount"], r["currency"], r["transaction_type"], r["status"],
                r["location"]["city"], r["location"]["country"],
                r["payment_method"], r["product_category"], r["quantity"],
                r["shipping_address"]["street"], r["shipping_address"]["zip"],
                r["shipping_address"]["city"], r["shipping_address"]["country"],
                r["device_info"]["os"], r["device_info"]["browser"], r["device_info"]["ip_address"],
                r["customer_rating"], r["discount_code"], r["tax_amount"],
                r["thread"], r["message_number"], r["timestamp_of_reception_log"]
            )
            cursor.execute(insert_query, values)
            db.commit()
            print(" Transaction insérée.")
        except Exception:
            print(" Erreur d’insertion dans MySQL :")
            traceback.print_exc()

if __name__ == "__main__":
    main()
