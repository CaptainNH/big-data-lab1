from confluent_kafka import Consumer, KafkaError
import pandas as pd
import json
import streamlit as st
import matplotlib.pyplot as plt
import time

bootstrap_servers = 'localhost:9095'
topic = 'info'

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'streamlit-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([topic])

st.title("Real-time Laptop Price Visualization")

# Создаем placeholder для графиков
chart_placeholder = st.empty()

# Список для хранения данных
data = []

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Чтение данных
        value = json.loads(msg.value())
        data.append(value)
        print(f"Received: {value}")

        # Ограничение количества данных для отображения
        if len(data) > 100:
            data = data[-100:]

        # Преобразование данных в DataFrame
        df = pd.DataFrame(data)

        # Создание графиков
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # График 1: Распределение цен
        axes[0, 0].hist(df['Price ($)'], bins=20, color='blue', alpha=0.7)
        axes[0, 0].set_title('Distribution of Laptop Prices')
        axes[0, 0].set_xlabel('Price')
        axes[0, 0].set_ylabel('Frequency')

        # График 2: Зависимость цены от оперативной памяти
        axes[0, 1].scatter(df['RAM (GB)'], df['Price ($)'], color='green', alpha=0.7)
        axes[0, 1].set_title('Price vs RAM')
        axes[0, 1].set_xlabel('RAM (GB)')
        axes[0, 1].set_ylabel('Price ($)')

        # График 3: Зависимость цены от GPU
        axes[1, 0].scatter(df['GPU'], df['Price ($)'], color='green', alpha=0.7)
        axes[1, 0].set_title('Price vs GPU')
        axes[1, 0].set_xlabel('GPU')
        axes[1, 0].set_ylabel('Price ($)')

        # График 4: Зависимость цены от CPU
        axes[1, 1].scatter(df['Processor'], df['Price ($)'], color='green', alpha=0.7)
        axes[1, 1].set_title('Price vs CPU')
        axes[1, 1].set_xlabel('Processor')
        axes[1, 1].set_ylabel('Price ($)')

        # # График 5: Зависимость цены от CPU
        # axes[4].scatter(df['Processor'], df['Price ($)'], color='green', alpha=0.7)
        # axes[4].set_title('Price vs RAM')
        # axes[4].set_xlabel('Processor')
        # axes[4].set_ylabel('Price ($)')

        # Отображение графиков в Streamlit
        chart_placeholder.pyplot(fig)

        # Очистка фигуры для следующего обновления
        plt.close(fig)

        time.sleep(0.1)  # Задержка для имитации реального времени

except KeyboardInterrupt:
    pass
finally:
    consumer.close()