import sqlite3

DB_NAME = "grades.db"

def initialize_database():
    connection = sqlite3.connect(DB_NAME)
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

def add_grade():
    print("-" * 30)
    print("NEUE NOTE EINTRAGEN")
    
    u_subject = input("Welches Fach? ")
    try:
        #Error Prevention
        u_grade = float(input("Welche Note? (z.B. 1.5): "))
    except ValueError:
        print("Fehler: Bitte eine Zahl eingeben!")
        return

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    sql_command = "INSERT INTO grades (subject, grade) VALUES (?, ?)"
    cursor.execute(sql_command, (u_subject, u_grade))
    
    connection.commit()
    connection.close()
    print("-> Gespeichert!")

def show_grades():
    print("-" * 30)
    print("DEINE NOTENÜBERSICHT")
    
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM grades")
    all_data = cursor.fetchall()
    
    if not all_data:
        print("Noch keine Noten gespeichert.")
    else:
        for row in all_data:
            print(f"Fach: {row[1]} | Note: {row[2]}")
            
    connection.close() 

    
def calculate_average():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    
    cursor.execute("SELECT grade FROM grades")
    results = cursor.fetchall()
    
    if not results:
        print("Kann keinen Durchschnitt berechnen (Keine Noten da).")
        connection.close()
        return
    
    total_sum = 0
    count = 0
    for row in results:
        grade_value = row[0]
        total_sum += grade_value
        count += 1
    average = total_sum / count
    
    print("-" * 30)
    print(f"Dein Durchscnitt: {average:.2f}")
    
    connection.close()
    
    
if __name__ == "__main__":   
    initialize_database()
    
    while True:
        print("\n" + "="*30)
        print(" Noten-Manager Menu")
        print("="*30)
        print("1: Neue Note eintragen")
        print("2: Alle Noten anzeigen")
        print("3: Durchschnitt berechnen")
        print("4: Programm beenden")
        
        selection = input("\nWas möchstest du tun? (1-4): ")
        
        if selection == "1":
            add_grade()
        elif selection == "2":
            show_grades()
        elif selection == "3":
            calculate_average()
        elif selection == "4":
            print("Bis zum nächsten Mal.")
            break
        else:
            print("Bitte 1, 2, 3 oder 4 drücken.")