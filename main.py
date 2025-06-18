import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
from model.model import ContactModel

# Inicializa o modelo
model = ContactModel()

# Create the main application window
app = tk.Tk()
app.title("Contact Management App")

# Global variables for pagination and search results
current_page = 1
page_size = 50
search_query = ""

# Functions for CRUD operations
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if name:
        model.add_contact(name, phone, email, address)
        clear_entries()
        display_contacts()
    else:
        messagebox.showerror("Error", "Name field is required.")

def edit_contact(event=None):
    selected_contact = contact_tree.selection()
    if selected_contact:
        contact_id = contact_tree.item(selected_contact, 'values')[0]
        new_name = name_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()
        new_address = address_entry.get()
        
        if contact_id:
            model.update_contact(contact_id, new_name, new_phone, new_email, new_address)
            clear_entries()
            display_contacts()
            messagebox.showinfo("Edit Successful", "Contact edited successfully.")
    else:
        messagebox.showerror("Error", "Please select a contact to edit.")

def delete_contact(event):
    selected_contact = contact_tree.selection()
    if selected_contact:
        contact_id = contact_tree.item(selected_contact, 'values')[0]
        model.delete_contact(contact_id)
        display_contacts()
    else:
        messagebox.showerror("Error", "Please select a contact to delete.")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def display_contacts():
    global current_page, search_query
    offset = (current_page - 1) * page_size
    contacts = model.get_contacts(offset, page_size, search_query)
    total_contacts = model.count_contacts(search_query)
    
    contact_tree.delete(*contact_tree.get_children())
    
    for contact in contacts:
        contact_tree.insert('', 'end', values=contact)
    
    # Calculate the total number of pages


def import_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        success, msg = model.import_csv(file_path)
        if success:
            global current_page
            current_page = 1
            display_contacts()
            messagebox.showinfo("Import Successful", msg)
        else:
            messagebox.showerror("Error", msg)

def next_page():
    global current_page
    current_page += 1
    display_contacts()

def prev_page():
    global current_page
    if current_page > 1:
        current_page -= 1
        display_contacts()

def search_contacts():
    global current_page, search_query
    search_query = search_entry.get()
    current_page = 1
    display_contacts()

def display_about_info():
    about_info = """
    Contact Management App

    Description:
    This application allows you to manage your contacts.

    Creator: Swathik Devadiga
    Version: 1.0
    Last Modified: {}
    """.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    messagebox.showinfo("About", about_info)

def on_double_click(event):
    item = contact_tree.selection()
    if item:
        contact_id = contact_tree.item(item, 'values')[0]
        if contact_id:
            contact = model.get_contact_by_id(contact_id)
            if contact:
                # Preenche o formulário com os dados do contato
                clear_entries()
                name_entry.insert(0, contact[1])
                phone_entry.insert(0, contact[2])
                email_entry.insert(0, contact[3])
                address_entry.insert(0, contact[4])

# UI Components
create_frame = ttk.Frame(app)
create_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

name_label = tk.Label(create_frame, text="Name:")
name_label.grid(row=0, column=0)
name_entry = ttk.Entry(create_frame)
name_entry.grid(row=1, column=0)

phone_label = tk.Label(create_frame, text="Phone:")
phone_label.grid(row=0, column=1)
phone_entry = ttk.Entry(create_frame)
phone_entry.grid(row=1, column=1)

email_label = tk.Label(create_frame, text="Email:")
email_label.grid(row=0, column=2)
email_entry = ttk.Entry(create_frame)
email_entry.grid(row=1, column=2)

address_label = tk.Label(create_frame, text="Address:")
address_label.grid(row=0, column=3)
address_entry = ttk.Entry(create_frame)
address_entry.grid(row=1, column=3)

add_button = ttk.Button(create_frame, text="Add Contact", command=add_contact)
add_button.grid(row=4, columnspan=4, pady=5)

search_frame = ttk.Frame(app)
search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

search_entry = ttk.Entry(search_frame)
search_entry.grid(row=1, column=1)

search_button = ttk.Button(search_frame, text="Search", command=search_contacts)
search_button.grid(row=1, column=2, padx=5)

about_button = ttk.Button(app, text="About", command=display_about_info)
about_button.grid(row=0, column=2, padx=10, pady=5, sticky="ne")

contact_tree = ttk.Treeview(app, columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")
contact_tree.heading("ID", text="ID")
contact_tree.heading("Name", text="Name")
contact_tree.heading("Phone", text="Phone")
contact_tree.heading("Email", text="Email")
contact_tree.heading("Address", text="Address")
contact_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

import_csv_button = ttk.Button(app, text="Import CSV", command=import_csv)
import_csv_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

prev_button = ttk.Button(app, text="Previous Page", command=prev_page)
prev_button.grid(row=2, column=0, sticky='w', padx=10, pady=5)

next_button = ttk.Button(app, text="Next Page", command=next_page)
next_button.grid(row=2, column=2, sticky='e', padx=10, pady=5)

status_label = tk.Label(app, text="", anchor="e")
status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="e")

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

contact_tree.bind("<Double-1>", on_double_click)

def contact_tree_popup(event):
    popup_menu = tk.Menu(app, tearoff=0)
    popup_menu.add_command(label="Edit Contact", command=lambda: on_double_click(event))
    popup_menu.add_command(label="Delete Contact", command=lambda: delete_contact(event))
    popup_menu.post(event.x_root, event.y_root)

contact_tree.bind("<Button-3>", contact_tree_popup)

display_contacts()
app.mainloop()
model.close()