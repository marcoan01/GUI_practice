import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random

def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table'")
    all_tables = cursor.fetchall()
    idx = random.randint(0, len(all_tables) - 1)
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name)
    table_records = cursor.fetchall()
    connection.close()
    return table_name, table_records

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def pre_process(table_name, table_records):
    ingredients = []
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])
    for i in table_records:
        name = i[1]
        quantity = i[2]
        unit = i[3]
        ingredients.append(quantity + " " + unit + " " + name)
    
    return title, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    logo_image = ImageTk.PhotoImage(file='assets/RRecipe_logo.png')
    logo_widget = tk.Label(frame1, image = logo_image, bg=bg_color)
    logo_widget.image = logo_image
    logo_widget.pack()
    text_label = tk.Label(frame1, text = "Ready for your random recipe?", bg=bg_color, fg="white", font=("fonts/Shanti-Regular.ttf", 14)).pack()
    tk.Button(frame1, text="SHUFFLE", font=("TkHeadingFont",20), bg="#28393a", fg="white", cursor='hand2', activebackground="#badee2", activeforeground="black", command=lambda:load_frame2()).pack()

def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()
    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)
    logo_image = ImageTk.PhotoImage(file='assets/RRecipe_logo_bottom.png')
    logo_widget = tk.Label(frame2, image = logo_image, bg=bg_color)
    logo_widget.image = logo_image
    logo_widget.pack(pady = 20)
    tk.Label(frame2, text = title, bg=bg_color, fg="white", font=("fonts/Shanti-Regular.ttf", 20)).pack(pady = 25)
    for i in ingredients:
        tk.Label(frame2, text = i, bg="#28393a", fg="white", font=("fonts/Shanti-Regular.ttf", 12)).pack(fill="both")
    
    tk.Button(frame2, text="BACK", font=("TkHeadingFont",18), bg="#28393a", fg="white", cursor='hand2', activebackground="#badee2", activeforeground="black", command=lambda:load_frame1()).pack(pady = 20)

bg_color = "#3d6466"
root = tk.Tk()
root.title("Recipe Pickers")
root.eval("tk::PlaceWindow . center")

frame1 = tk.Frame(root, width = 500, height = 600, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)

for frame in(frame1, frame2):
    frame.grid(row=0, column=0, sticky='nesw')

load_frame1()

root.mainloop()