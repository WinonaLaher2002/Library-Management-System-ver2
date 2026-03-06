import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import subprocess
from supabase_db import get_book_by_id, update_book

def return_book():
    book_id = book_id_entry.get()
    return_time = return_time_entry.get()

    if book_id and return_time:
        try:
            result = get_book_by_id(book_id)
            
            if result:
                quantity = result["quantity"]
                return_time_dt = datetime.strptime(return_time, "%m/%d/%Y")
                update_book(
                    book_id,
                    {"quantity": quantity + 1, "return_time": return_time_dt.isoformat()},
                )
                messagebox.showinfo("Success", "The book is returned.")
            else:
                messagebox.showerror("Error", "Book ID not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def back_to_user_panel():
    root.destroy()  # Close the return book window
    subprocess.Popen(["python", "userview.py"])  # Open userview.py

root = tk.Tk()
root.title("Return Book")

# Set background color
root.configure(bg="#E3FEF7")

# Header Label
header_label = tk.Label(root, text="Return Book", font=("Arial", 18, "bold"), bg="#E3FEF7", fg="#003C43")
header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Labels and Entry Fields
labels = ["Book ID", "Return Date (MM/DD/YYYY)"]
entries = []

for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text + ":", bg="#E3FEF7", fg="#003C43")
    label.grid(row=i+1, column=0, padx=10, pady=3, sticky="w")
    entry = tk.Entry(root)
    entry.grid(row=i+1, column=1, padx=10, pady=3, sticky="ew")
    entries.append(entry)

book_id_entry, return_time_entry = entries

# Buttons
buttons = [("Return Book", return_book), ("Back to User Panel", back_to_user_panel)]

for i, (button_text, command) in enumerate(buttons):
    button = tk.Button(root, text=button_text, command=command, fg="white", bg="#135D66")
    button.grid(row=i+len(labels)+1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Set screen size and position after all elements have been placed
root.geometry("360x300")

root.mainloop()
