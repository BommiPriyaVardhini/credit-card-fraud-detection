import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Drop existing transactions table if it exists (to avoid conflicts)
cursor.execute("DROP TABLE IF EXISTS transactions")

# Create a new transactions table with the correct columns
cursor.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        card_number TEXT NOT NULL,
        validity TEXT NOT NULL,
        transaction_date TEXT NOT NULL,
        transaction_time TEXT NOT NULL,
        amount REAL NOT NULL,
        fraud_status TEXT NOT NULL
    )
""")

print("Transactions table recreated successfully.")

conn.commit()
conn.close()
