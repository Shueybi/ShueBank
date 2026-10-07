import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shuebank.db")


def get_connection():
    return sqlite3.connect(DATABASE)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            account_number TEXT UNIQUE NOT NULL,
            balance REAL DEFAULT 0,
            role TEXT NOT NULL DEFAULT "user",
            status TEXT NOT NULL DEFAULT "active"
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("ShueBank database created successfully.")
