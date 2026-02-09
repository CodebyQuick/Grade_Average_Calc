#CREATE DATABANK
import sqlite3

connection = sqlite3.connect("grades.db")

cursor = connection.cursor()

sql_blueprint = """
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    grade REAL
)
"""
cursor.execute(sql_blueprint)

connection.commit()
connection.close()

print("Done! Databank 'grades.db' was created.")