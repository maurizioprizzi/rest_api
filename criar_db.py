import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Cria a tabela "categories" no banco de dados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

conn.commit()
conn.close()
