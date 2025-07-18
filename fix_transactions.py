import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Function to check if a column exists
def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    return column_name in columns

# Add fraud_status column if it does not exist
if not column_exists(cursor, "transactions", "fraud_status"):
    cursor.execute("ALTER TABLE transactions ADD COLUMN fraud_status TEXT DEFAULT 'Pending'")
    print("✅ Column 'fraud_status' added successfully.")
else:
    print("⚠️ Column 'fraud_status' already exists.")

# Add status column if it does not exist
if not column_exists(cursor, "transactions", "status"):
    cursor.execute("ALTER TABLE transactions ADD COLUMN status TEXT DEFAULT 'Unknown'")
    print("✅ Column 'status' added successfully.")

    # Update existing rows to avoid NULL constraint issues
    cursor.execute("UPDATE transactions SET status = 'Unknown' WHERE status IS NULL")
    print("✅ Updated existing records with default status 'Unknown'.")
else:
    print("⚠️ Column 'status' already exists.")

# Commit changes and close connection
conn.commit()
conn.close()
print("✅ Database update completed!")
