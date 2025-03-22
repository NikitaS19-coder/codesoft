import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Database setup
conn = sqlite3.connect("contacts.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        address TEXT
    )
""")
conn.commit()

# Functions
def add_contact():
    store_name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    if store_name and phone:
        cursor.execute("INSERT INTO contacts (store_name, phone, email, address) VALUES (?, ?, ?, ?)",
                       (store_name, phone, email, address))
        conn.commit()
        messagebox.showinfo("Success", "Contact added successfully")
        clear_entries()
        display_contacts()
    else:
        messagebox.showwarning("Error", "Store Name and Phone are required")

def display_contacts():
    for item in tree.get_children():
        tree.delete(item)
    
    cursor.execute("SELECT id, store_name, phone FROM contacts")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def search_contact():
    query = entry_search.get()
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT id, store_name, phone FROM contacts WHERE store_name LIKE ? OR phone LIKE ?", 
                   ('%' + query + '%', '%' + query + '%'))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def update_contact():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Select a contact to update")
        return

    item = tree.item(selected)
    contact_id = item["values"][0]

    store_name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()

    cursor.execute("UPDATE contacts SET store_name=?, phone=?, email=?, address=? WHERE id=?",
                   (store_name, phone, email, address, contact_id))
    conn.commit()
    messagebox.showinfo("Success", "Contact updated")
    clear_entries()
    display_contacts()

def delete_contact():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Select a contact to delete")
        return

    item = tree.item(selected)
    contact_id = item["values"][0]

    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    messagebox.showinfo("Deleted", "Contact deleted successfully")
    display_contacts()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Contact Management System")
root.geometry("600x500")

# Labels and Entries
tk.Label(root, text="Store Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
entry_phone = tk.Entry(root)
entry_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Address:").grid(row=3, column=0, padx=5, pady=5)
entry_address = tk.Entry(root)
entry_address.grid(row=3, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Contact", command=add_contact).grid(row=4, column=0, pady=10)
tk.Button(root, text="Update Contact", command=update_contact).grid(row=4, column=1, pady=10)
tk.Button(root, text="Delete Contact", command=delete_contact).grid(row=5, column=0, pady=10)
tk.Button(root, text="Clear", command=clear_entries).grid(row=5, column=1, pady=10)

# Search Bar
tk.Label(root, text="Search:").grid(row=6, column=0, padx=5, pady=5)
entry_search = tk.Entry(root)
entry_search.grid(row=6, column=1, padx=5, pady=5)
tk.Button(root, text="Search", command=search_contact).grid(row=6, column=2, padx=5, pady=5)

# Contact List Table
tree = ttk.Treeview(root, columns=("ID", "Store Name", "Phone"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Store Name", text="Store Name")
tree.heading("Phone", text="Phone")
tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

# Load contacts
display_contacts()

# Run the App
root.mainloop()
