import sqlite3
import pandas as pd


# =========================================
# CREATE DATABASE
# =========================================

def create_database():

    conn = sqlite3.connect("inventory.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS medicines (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        strength TEXT,

        use TEXT,

        side_effect TEXT,

        dosage TEXT,

        expiry TEXT

    )

    """)

    conn.commit()

    conn.close()

    print("Table Created")


# =========================================
# INSERT CSV DATA
# =========================================

def insert_from_csv():

    conn = sqlite3.connect("inventory.db")

    cursor = conn.cursor()

    cursor.execute("DELETE FROM medicines")

    data = pd.read_csv("medicine_database.csv")

    for index, row in data.iterrows():

        cursor.execute(

            """

            INSERT INTO medicines

            (name, strength, use, side_effect, dosage, expiry)

            VALUES (?, ?, ?, ?, ?, ?)

            """,

            (

                row['name'],

                row['strength'],

                row['use'],

                row['side_effect'],

                row['dosage'],

                row['expiry']

            )

        )

    conn.commit()

    conn.close()

    print("Data Inserted")


# =========================================
# SEARCH MEDICINE
# =========================================

def search_medicine(name):

    conn = sqlite3.connect("inventory.db")

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM medicines WHERE LOWER(name) LIKE LOWER(?)",

        ('%' + name + '%',)

    )

    result = cursor.fetchone()

    conn.close()

    if result:

        return {

            "name": result[1],

            "strength": result[2],

            "use": result[3],

            "side_effect": result[4],

            "dosage": result[5],

            "expiry": result[6]

        }

    return None