import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INTEGER PRIMARY KEY,
        quantity INTEGER
    )
''')

conn.commit()
conn.close()
