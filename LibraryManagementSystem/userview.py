import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
from supabase_db import add_book as add_book_record, delete_book as delete_book_record, get_books

def add_book():
    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    quantity = quantity_entry.get()

    if title and author and isbn and quantity:
        try:
            add_book_record(book_id, title, author, isbn, quantity)
            messagebox.showinfo("Success", "Book added successfully!")
            display_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def display_books():
    treeview.delete(*treeview.get_children())
    for book in get_books():
        borrowed_time = "Not Borrowed!" if not book["borrowed_time"] else book["borrowed_time"].strftime("%m/%d/%Y")
        return_time = book["return_time"].strftime("%m/%d/%Y") if book["return_time"] else "Not Returned!"
        treeview.insert("", "end", values=(book["book_id"], book["title"], book["author"], book["isbn"], book["quantity"], borrowed_time, return_time))

def borrow_book():
    subprocess.Popen(["python", "borrowBook.py"])

def return_book():
    subprocess.Popen(["python", "returnBook.py"])

def search_books():
    search_term = search_entry.get() or ""
    treeview.delete(*treeview.get_children())
    for book in get_books(search_term):
        borrowed_time = "Not Borrowed!" if not book["borrowed_time"] else book["borrowed_time"].strftime("%m/%d/%Y")
        return_time = book["return_time"].strftime("%m/%d/%Y") if book["return_time"] else "Not Returned!"
        treeview.insert("", "end", values=(book["book_id"], book["title"], book["author"], book["isbn"], book["quantity"], borrowed_time, return_time))

def reset_fields():
    for entry in entries:
        entry.delete(0, tk.END)

def delete_book():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a book to delete.")
        return
    
    book_id = treeview.item(selected_item, 'values')[0]
    try:
        delete_book_record(book_id)
        messagebox.showinfo("Success", "Book deleted successfully!")
        display_books()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def logout():
    root.destroy()

root = tk.Tk()
root.title("User Panel")
root.configure(bg="#E3FEF7")

header_label = tk.Label(root, text="Library Management System", font=("Arial", 18, "bold"), bg="#E3FEF7", fg="#003C43")
header_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

labels = ["Book ID:", "Title:", "Author:", "ISBN:", "Quantity:"]
entries = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text, bg="#E3FEF7", fg="#003C43")
    label.grid(row=i+1, column=0, padx=10, pady=3, sticky="w")
    entry = tk.Entry(root)
    entry.grid(row=i+1, column=1, padx=10, pady=3, sticky="ew")
    entries.append(entry)

book_id_entry, title_entry, author_entry, isbn_entry, quantity_entry = entries

buttons = [("Add Book", add_book), ("Display Books", display_books), ("Borrow Book", borrow_book), ("Return Book", return_book),("Logout", logout)]

for i, (button_text, command) in enumerate(buttons):
    button = tk.Button(root, text=button_text, command=command, fg="white", bg="#135D66")
    button.grid(row=i+1, column=2, padx=10, pady=5, sticky="ew")

search_label = tk.Label(root, text="Search:", bg="#E3FEF7", fg="#003C43")
search_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
search_entry = tk.Entry(root)
search_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

search_button = tk.Button(root, text="Search", command=search_books, fg="white", bg="#135D66")
search_button.grid(row=8, column=2, padx=10, pady=5, sticky="ew")

reset_button = tk.Button(root, text="Reset", command=reset_fields, fg="white", bg="#135D66")
reset_button.grid(row=9, column=0, columnspan=3, padx=10, pady=5, sticky="ew")


# Adding columns to the treeview
treeview_columns = ["Book ID", "Title", "Author", "ISBN", "Quantity", "Borrowed Time", "Return Time"]
treeview = ttk.Treeview(root, columns=treeview_columns, show="headings", selectmode="browse")
for col in treeview_columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)

treeview.grid(row=10, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

for i in range(11):
    root.grid_rowconfigure(i, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

root.geometry("1920x1080")
root.mainloop()
