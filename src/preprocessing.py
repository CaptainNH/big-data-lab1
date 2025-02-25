import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Загрузка данных
df = pd.read_csv('../laptop_prices.csv')

# Предобработка данных

# Кодирование категориальных переменных
categorical_cols = ['Brand', 'Processor', 'RAM (GB)', 'Storage', 'GPU', 'Screen Size (inch)', 'Resolution', 'Battery Life (hours)', 'Weight (kg)', 'Operating System']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Сохранение обработанных данных
df.to_csv('processed_laptop_prices.csv', index=False)