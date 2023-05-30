import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Cria a tabela "products" no banco de dados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity INTEGER,
        category_id INTEGER,
        category_name TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
''')

conn.commit()
conn.close()