import sqlite3

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criação da tabela "users"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        senha TEXT
    )
''')

# Criação da tabela "products"
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

# Criação da tabela "inventory"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INTEGER PRIMARY KEY,
        quantity INTEGER,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')

# Criação da tabela "categories"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

conn.commit()
conn.close()

