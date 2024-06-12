import sqlite3
import pandas as pd

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    date TEXT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
''')


data = [
    ('2024-06-01', 'Product A', 10, 9.99),
    ('2024-06-01', 'Product B', 5, 19.99),
    ('2024-06-02', 'Product A', 700, 9.99),
    ('2024-06-02', 'Product B', 3, 19.99),
    
]

cursor.executemany('INSERT INTO sales (date, product, quantity, price) VALUES (?, ?, ?, ?)', data)
conn.commit()

conn.close()
