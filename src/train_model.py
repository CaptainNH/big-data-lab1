from confluent_kafka import Consumer, KafkaError
import pandas as pd
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

bootstrap_servers = 'localhost:9095'
topic = 'info'

conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'ml-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([topic])

data = []

def train_model(data):
    df = pd.DataFrame(data)
    if len(df) < 10:  # Минимум 10 записей для обучения
        return

    # Предположим, что целевая переменная - 'Price'
    X = df.drop(columns=['Price ($)'])
    y = df['Price ($)']

    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Обучение модели
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Оценка модели
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model MAE: {mae}")

    # Сохранение модели
    joblib.dump(model, 'laptop_price_model.pkl')

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

        # Обучение модели каждые 100 сообщений
        if len(data) >= 100:
            train_model(data)
            data = []  # Очистка данных после обучения

except KeyboardInterrupt:
    pass
finally:
    consumer.close()