import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk # ttk macht die Buttons hübscher

DB_NAME = "grades.db"


def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        grade REAL
    )
    """)
    conn.commit()
    conn.close()

def save_grade():
    fach = entry_fach.get()
    note_text = entry_note.get()

    if not fach or not note_text:
        messagebox.showwarning("Fehler", "Bitte beide Felder ausfüllen!")
        return

    try:
        note = float(note_text.replace(",", "."))
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO grades (subject, grade) VALUES (?, ?)", (fach, note))
        conn.commit()
        conn.close()
        
        
        entry_fach.delete(0, tk.END)
        entry_note.delete(0, tk.END)
        messagebox.showinfo("Erfolg", f"Note für {fach} gespeichert!")
        update_list() 
        
    except ValueError:
        messagebox.showerror("Fehler", "Die Note muss eine Zahl sein (z.B. 2.5)")

def update_list():
    listbox.delete(0, tk.END)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    rows = cursor.fetchall()
    
    total = 0
    count = 0
    
    for row in rows:
        text = f"{row[1]}: {row[2]}"
        listbox.insert(tk.END, text)
        total += row[2]
        count += 1
    
    conn.close()
    
    
    if count > 0:
        avg = total / count
        label_average.config(text=f"Durchschnitt: {avg:.2f}")
    else:
        label_average.config(text="Durchschnitt: -")


window = tk.Tk()
window.title("Noten-Manager Pro")
window.geometry("400x500")

label_title = tk.Label(window, text="Meine Notenverwaltung", font=("Arial", 16, "bold"))
label_title.pack(pady=10)


frame_input = tk.Frame(window)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Fach:").grid(row=0, column=0, padx=5)
entry_fach = tk.Entry(frame_input)
entry_fach.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Note:").grid(row=1, column=0, padx=5)
entry_note = tk.Entry(frame_input)
entry_note.grid(row=1, column=1, padx=5)

btn_save = tk.Button(window, text="Note speichern", command=save_grade, bg="#4CAF50", fg="white")
btn_save.pack(pady=10, fill="x", padx=50)

listbox = tk.Listbox(window)
listbox.pack(fill="both", expand=True, padx=20, pady=5)


label_average = tk.Label(window, text="Durchschnitt: -", font=("Arial", 12, "bold"))
label_average.pack(pady=10)

initialize_database() 
update_list()         
window.mainloop()  