import sqlite3

# Connect to the local SQLite database file
conn = sqlite3.connect("aisys_library.db")
cursor = conn.cursor()

# Query and print all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables in database:", cursor.fetchall())

# Close the connection
conn.close()