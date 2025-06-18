import tkinter as tk
from tkinter import ttk

class ContactView:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management App")
        self.create_widgets()
    
    def create_widgets(self):
        # Create Form Frame
        self.create_frame = ttk.Frame(self.root)
        self.create_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Name Field
        self.name_label = tk.Label(self.create_frame, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = ttk.Entry(self.create_frame)
        self.name_entry.grid(row=1, column=0)
        
        # Phone Field
        self.phone_label = tk.Label(self.create_frame, text="Phone:")
        self.phone_label.grid(row=0, column=1)
        self.phone_entry = ttk.Entry(self.create_frame)
        self.phone_entry.grid(row=1, column=1)
        
        # Email Field
        self.email_label = tk.Label(self.create_frame, text="Email:")
        self.email_label.grid(row=0, column=2)
        self.email_entry = ttk.Entry(self.create_frame)
        self.email_entry.grid(row=1, column=2)
        
        # Address Field
        self.address_label = tk.Label(self.create_frame, text="Address:")
        self.address_label.grid(row=0, column=3)
        self.address_entry = ttk.Entry(self.create_frame)
        self.address_entry.grid(row=1, column=3)
        
        # Add Button
        self.add_button = ttk.Button(self.create_frame, text="Add Contact")
        self.add_button.grid(row=4, column=0, pady=5, sticky='w')
        
        # Delete Button (novo)
        self.delete_button = ttk.Button(self.create_frame, text="Delete Selected")
        self.delete_button.grid(row=4, column=1, pady=5, padx=5)
        
        # Clear Button (para manter o layout balanceado)
        self.clear_button = ttk.Button(self.create_frame, text="Clear Form")
        self.clear_button.grid(row=4, column=2, pady=5)
        
        # Search Frame
        self.search_frame = ttk.Frame(self.root)
        self.search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # Search Field
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.grid(row=1, column=1)
        
        # Search Button
        self.search_button = ttk.Button(self.search_frame, text="Search")
        self.search_button.grid(row=1, column=2, padx=5)
        
        # About Button
        self.about_button = ttk.Button(self.root, text="About")
        self.about_button.grid(row=0, column=2, padx=10, pady=5, sticky="ne")
        
        # Contact Tree
        self.contact_tree = ttk.Treeview(
            self.root, 
            columns=("ID", "Name", "Phone", "Email", "Address"), 
            show="headings"
        )
        self.contact_tree.heading("ID", text="ID")
        self.contact_tree.heading("Name", text="Name")
        self.contact_tree.heading("Phone", text="Phone")
        self.contact_tree.heading("Email", text="Email")
        self.contact_tree.heading("Address", text="Address")
        self.contact_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Import CSV Button
        self.import_csv_button = ttk.Button(self.root, text="Import CSV")
        self.import_csv_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        
        # Export CSV Button
        self.export_csv_button = ttk.Button(self.root, text="Export CSV")
        self.export_csv_button.grid(row=0, column=2, padx=(0, 100), pady=5, sticky="e")
        
        # Pagination Buttons
        self.prev_button = ttk.Button(self.root, text="Previous Page")
        self.prev_button.grid(row=2, column=0, sticky='w', padx=10, pady=5)
        
        self.next_button = ttk.Button(self.root, text="Next Page")
        self.next_button.grid(row=2, column=2, sticky='e', padx=10, pady=5)
        
        # Status Label
        self.status_label = tk.Label(self.root, text="", anchor="e")
        self.status_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="e")
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def get_form_data(self):
        return {
            'name': self.name_entry.get(),
            'phone': self.phone_entry.get(),
            'email': self.email_entry.get(),
            'address': self.address_entry.get()
        }
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
    
    def get_selected_contact_id(self):
        selected_item = self.contact_tree.selection()
        if selected_item:
            return self.contact_tree.item(selected_item, 'values')[0]
        return None
    
    def display_contacts(self, contacts):
        self.contact_tree.delete(*self.contact_tree.get_children())
        for contact in contacts:
            self.contact_tree.insert('', 'end', values=contact)
    
    def set_status(self, text):
        self.status_label.config(text=text)
    
    def get_search_query(self):
        return self.search_entry.get()
    
    def bind_events(self, callbacks):
        self.add_button.config(command=callbacks['add_contact'])
        self.delete_button.config(command=callbacks['delete_contact'])
        self.clear_button.config(command=callbacks['clear_form'])
        self.search_button.config(command=callbacks['search_contacts'])
        self.about_button.config(command=callbacks['display_about'])
        self.import_csv_button.config(command=callbacks['import_csv'])
        self.export_csv_button.config(command=callbacks['export_csv'])
        self.prev_button.config(command=callbacks['prev_page'])
        self.next_button.config(command=callbacks['next_page'])
        self.contact_tree.bind("<Double-1>", callbacks['on_double_click'])
        self.contact_tree.bind("<Button-3>", callbacks['on_right_click'])