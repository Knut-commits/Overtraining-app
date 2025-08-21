import sqlite3

# Connect to your database file
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# View data from a table (replace 'User' with your table name)
table_name = 'User'  # Change to the table you want to view
cursor.execute(f"SELECT * FROM {table_name};")
rows = cursor.fetchall()
print(f"Rows in {table_name}:", rows)

conn.close()