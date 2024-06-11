import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


def create_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                 (id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  email TEXT,
                  address TEXT)''')
    conn.commit()
    conn.close()

def add_contact(name, phone, email, address):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)', (name, phone, email, address))
    conn.commit()
    conn.close()

def view_contacts():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    contacts = c.fetchall()
    conn.close()
    return contacts

def search_contacts(search_term):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?', ('%' + search_term + '%', '%' + search_term + '%'))
    contacts = c.fetchall()
    conn.close()
    return contacts

def update_contact(contact_id, name, phone, email, address):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?', (name, phone, email, address, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
    conn.commit()
    conn.close()


def add_contact_ui():
    def save_contact():
        name = name_var.get()
        phone = phone_var.get()
        email = email_var.get()
        address = address_var.get()
        add_contact(name, phone, email, address)
        messagebox.showinfo("Success", "Contact added successfully")
        add_window.destroy()
        refresh_contacts()

    add_window = tk.Toplevel(root)
    add_window.title("Add Contact")

    tk.Label(add_window, text="Name").grid(row=0, column=0)
    tk.Label(add_window, text="Phone").grid(row=1, column=0)
    tk.Label(add_window, text="Email").grid(row=2, column=0)
    tk.Label(add_window, text="Address").grid(row=3, column=0)

    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    address_var = tk.StringVar()

    tk.Entry(add_window, textvariable=name_var).grid(row=0, column=1)
    tk.Entry(add_window, textvariable=phone_var).grid(row=1, column=1)
    tk.Entry(add_window, textvariable=email_var).grid(row=2, column=1)
    tk.Entry(add_window, textvariable=address_var).grid(row=3, column=1)

    tk.Button(add_window, text="Save", command=save_contact, bg="green", fg="white").grid(row=4, column=1)

def view_contact_ui():
    contacts = view_contacts()
    contact_listbox.delete(0, tk.END)
    
    for contact in contacts:
        contact_str = f"Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}, Address: {contact[4]}"
        contact_listbox.insert(tk.END, contact_str)

def search_contact_ui():
    def perform_search():
        search_term = search_var.get()
        contacts = search_contacts(search_term)
        contact_listbox.delete(0, tk.END)

        for contact in contacts:
            contact_str = f"Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}, Address: {contact[4]}"
            contact_listbox.insert(tk.END, contact_str)

    search_window = tk.Toplevel(root)
    search_window.title("Search Contact")

    tk.Label(search_window, text="Search").grid(row=0, column=0)
    search_var = tk.StringVar()
    tk.Entry(search_window, textvariable=search_var).grid(row=0, column=1)
    tk.Button(search_window, text="Search", command=perform_search, bg="blue", fg="white").grid(row=0, column=2)

def update_contact_ui():
    def select_contact():
        contact_id = int(contact_id_var.get())
        contact = None
        contacts = view_contacts()
        for c in contacts:
            if c[0] == contact_id:
                contact = c
                break
        
        if contact:
            name_var.set(contact[1])
            phone_var.set(contact[2])
            email_var.set(contact[3])
            address_var.set(contact[4])
        else:
            messagebox.showerror("Error", "Contact not found")

    def save_update():
        contact_id = int(contact_id_var.get())
        name = name_var.get()
        phone = phone_var.get()
        email = email_var.get()
        address = address_var.get()
        update_contact(contact_id, name, phone, email, address)
        messagebox.showinfo("Success", "Contact updated successfully")
        update_window.destroy()
        refresh_contacts()

    update_window = tk.Toplevel(root)
    update_window.title("Update Contact")

    tk.Label(update_window, text="Contact ID").grid(row=0, column=0)
    contact_id_var = tk.StringVar()
    tk.Entry(update_window, textvariable=contact_id_var).grid(row=0, column=1)
    tk.Button(update_window, text="Select", command=select_contact, bg="orange", fg="white").grid(row=0, column=2)

    tk.Label(update_window, text="Name").grid(row=1, column=0)
    tk.Label(update_window, text="Phone").grid(row=2, column=0)
    tk.Label(update_window, text="Email").grid(row=3, column=0)
    tk.Label(update_window, text="Address").grid(row=4, column=0)

    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    address_var = tk.StringVar()

    tk.Entry(update_window, textvariable=name_var).grid(row=1, column=1)
    tk.Entry(update_window, textvariable=phone_var).grid(row=2, column=1)
    tk.Entry(update_window, textvariable=email_var).grid(row=3, column=1)
    tk.Entry(update_window, textvariable=address_var).grid(row=4, column=1)

    tk.Button(update_window, text="Update", command=save_update, bg="purple", fg="white").grid(row=5, column=1)

def delete_contact_ui():
    def perform_delete():
        contact_id = int(contact_id_var.get())
        delete_contact(contact_id)
        messagebox.showinfo("Success", "Contact deleted successfully")
        delete_window.destroy()
        refresh_contacts()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Contact")

    tk.Label(delete_window, text="Contact ID").grid(row=0, column=0)
    contact_id_var = tk.StringVar()
    tk.Entry(delete_window, textvariable=contact_id_var).grid(row=0, column=1)
    tk.Button(delete_window, text="Delete", command=perform_delete, bg="red", fg="white").grid(row=0, column=2)

def refresh_contacts():
    view_contact_ui()

# Main GUI setup
root = tk.Tk()
root.title("Contact Management")

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Contact", command=add_contact_ui, bg="pink", fg="black").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="View Contacts", command=view_contact_ui, bg="light blue", fg="black").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Search Contacts", command=search_contact_ui, bg="light yellow", fg="black").grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Update Contact", command=update_contact_ui, bg="light grey", fg="black").grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Delete Contact", command=delete_contact_ui, bg="light green", fg="black").grid(row=0, column=4, padx=5)

contact_list_frame = tk.Frame(root)
contact_list_frame.pack()

contact_listbox = tk.Listbox(contact_list_frame, width=100, height=20, bg="light grey")
contact_listbox.pack()

create_db()
view_contact_ui()

root.mainloop()
