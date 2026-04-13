import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        use TEXT,
        side_effect TEXT,
        dosage TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Table Created")


def insert_from_csv():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    data = pd.read_csv("medicine_database.csv")

    for index, row in data.iterrows():
        cursor.execute(
            "INSERT INTO medicines (name, use, side_effect, dosage) VALUES (?, ?, ?, ?)",
            (row['name'], row['use'], row['side_effect'], row['dosage'])
        )

    conn.commit()
    conn.close()
    print("Data Inserted")


def search_medicine(name):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medicines WHERE name=?", (name,))
    result = cursor.fetchone()

    conn.close()
    return result
