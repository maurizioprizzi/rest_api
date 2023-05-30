import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Cria a tabela "users" no banco de dados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        senha TEXT
    )
''')

conn.commit()
conn.close()
