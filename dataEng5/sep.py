import pandas as pd
import pickle

# Чтение исходного CSV файла
df = pd.read_csv('books.csv', on_bad_lines='skip')

# Разделение таблицы на две части (например, по столбцам или строкам)
# Для примера разделим по столбцам
half_len = len(df) // 2
df1 = df.iloc[:half_len] 
df2 = df.iloc[half_len:]

# Сохранение первой части в CSV файл
df1.to_csv('part1.csv', index=False)

# Сохранение второй части в PKL файл
with open('part2.pkl', 'wb') as f:
    pickle.dump(df2, f)

