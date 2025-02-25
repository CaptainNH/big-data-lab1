# from kafka import KafkaProducer
from confluent_kafka import Producer
import pandas as pd
import json
import time

# Загрузка данных
df = pd.read_csv('../processed_laptop_prices.csv')

bootstrap_servers = 'localhost:9095'
topic = 'info'

conf = {'bootstrap.servers': bootstrap_servers}

producer = Producer(conf)


def get_data(row):
    res = {
        # 'Type of info': "info",
    }

    combined_data = {**res, **row.to_dict()}

    return pd.Series(combined_data).to_json()


def produce_data():
    for index, row in df.iterrows():
        data = get_data(row)
        producer.produce(topic, key='1', value=data)
        producer.flush()
        print(f"Produced: {data}")
        time.sleep(0.1)


if __name__ == "__main__":
    produce_data()