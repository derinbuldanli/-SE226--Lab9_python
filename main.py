import datetime
import tkinter as tk
import sqlite3


conn = sqlite3.connect('mcu_movies.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        movie TEXT,
        date TEXT,
        mcu_phase TEXT
    )
''')
conn.commit()


with open('marvel.txt', 'r') as file:
    lines = file.readlines()

    for line in lines:
        data = line.strip().split('  ')
        id = int(data[0])
        movie = data[1]
        date_str = data[2].split(' ')[0]
        date = datetime.datetime.strptime(date_str, '%B%d,%Y').date()
        phase = data[3]

        cursor.execute('INSERT INTO movies (id, movie, date, mcu_phase) VALUES (?, ?, ?, ?)',
                       (id, movie, date, phase))
    conn.commit()



def add_button_clicked():
    popup = tk.Toplevel(root)
    entry = tk.Entry(popup)
    ok_button = tk.Button(popup, text="Ok", command=lambda: add_to_database(entry.get(), popup))
    cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
    entry.pack()
    ok_button.pack()
    cancel_button.pack()


def add_to_database(data, popup):
    conn = sqlite3.connect('mcu_movies.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO movies (id, movie, date, mcu_phase) VALUES (?, ?, ?, ?)',
                   (int(data.split()[0]), data.split()[1], data.split()[2], data.split()[3]))
    conn.commit()
    conn.close()
    popup.destroy()


def list_all_button_clicked():
    conn = sqlite3.connect('mcu_movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM movies')
    rows = cursor.fetchall()
    conn.close()
    text_box.delete(1.0, tk.END)
    for row in rows:
        text_box.insert(tk.END, f'{row[0]} {row[1]} {row[2]} {row[3]}\n')


root = tk.Tk()
ids = [str(i) for i in range(1, 23)]
selected_id = tk.StringVar(root)
dropdown = tk.OptionMenu(root, selected_id, *ids)
dropdown.pack()
text_box = tk.Text(root, width=40, height=10)
text_box.pack()
add_button = tk.Button(root, text="Add", command=add_button_clicked)
add_button.pack()
list_all_button = tk.Button(root, text="LIST ALL", command=list_all_button_clicked)
list_all_button.pack()
root.mainloop()


