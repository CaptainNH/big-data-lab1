# Лабораторная работа №1

## Набор данных
Используется набор данных https://www.kaggle.com/datasets/asinow/laptop-price-dataset/data
## ML задача
Решается задача регрессии. Предсказывается цена ноутбука на основе его характеристик

## Подготовка окружения
- Установите зависимости из requirements: `pip install -r requirements.txt`
- Скачайте docker образ kafka: `docker pull bitnami/kafka`
## Запуск
- Поднимите контейнер: `docker-compose up -d`
- Запустите по порядку скрипты в отдельных терминалах:
```
python src/preprocessing.py
python src/producer1.py
python src/producer2.py
python src/tran_model.py
streamlit run src/app.py
```
## Выключение
- Во всех консолях остановите работу скриптов через `Ctrl+C`
- Выполните `docker-compose down`
