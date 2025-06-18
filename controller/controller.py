from model.model import ContactModel
from view.view import ContactView
from tkinter import messagebox, filedialog
import datetime
from math import ceil

class ContactController:
    def __init__(self, root):
        self.model = ContactModel()
        self.view = ContactView(root)
        self.current_page = 1
        self.page_size = 50
        self.search_query = ""
        
        # Bind events
        self.view.bind_events({
            'add_contact': self.add_contact,
            'search_contacts': self.search_contacts,
            'display_about': self.display_about_info,
            'import_csv': self.import_csv,
            'export_csv': self.export_csv,
            'prev_page': self.prev_page,
            'next_page': self.next_page,
            'on_double_click': self.on_double_click,
            'on_right_click': self.contact_tree_popup
        })
        
        self.display_contacts()
    
    def add_contact(self):
        data = self.view.get_form_data()
        if data['name']:
            self.model.add_contact(
                data['name'], 
                data['phone'], 
                data['email'], 
                data['address']
            )
            self.view.clear_form()
            self.display_contacts()
        else:
            messagebox.showerror("Error", "Name field is required.")
    
    def edit_contact(self, contact_id):
        data = self.view.get_form_data()
        if contact_id:
            self.model.update_contact(
                contact_id,
                data['name'],
                data['phone'],
                data['email'],
                data['address']
            )
            self.view.clear_form()
            self.display_contacts()
            messagebox.showinfo("Edit Successful", "Contact edited successfully.")
    
    def delete_contact(self, contact_id):
        if contact_id:
            self.model.delete_contact(contact_id)
            self.display_contacts()
    
    def display_contacts(self):
        offset = (self.current_page - 1) * self.page_size
        contacts = self.model.get_contacts(offset, self.page_size, self.search_query)
        total_contacts = self.model.count_contacts(self.search_query)
        
        self.view.display_contacts(contacts)
        
        total_pages = ceil(total_contacts / self.page_size) if total_contacts > 0 else 1
        status_text = f"Page {self.current_page} of {total_pages} | Total Contacts: {total_contacts}"
        self.view.set_status(status_text)
    
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            success, msg = self.model.import_csv(file_path)
            if success:
                self.current_page = 1
                self.display_contacts()
                messagebox.showinfo("Import Successful", msg)
            else:
                messagebox.showerror("Error", msg)
    
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            success, msg = self.export_to_csv(file_path)
            if success:
                messagebox.showinfo("Export Successful", msg)
            else:
                messagebox.showerror("Error", msg)
    
    def export_to_csv(self, file_path):
        try:
            contacts = self.model.get_contacts(0, 10000)  # Get all contacts
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Address'])
                for contact in contacts:
                    writer.writerow(contact)
            return True, "Contacts exported successfully to CSV."
        except Exception as e:
            return False, f"Error exporting CSV: {str(e)}"
    
    def next_page(self):
        self.current_page += 1
        self.display_contacts()
    
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_contacts()
    
    def search_contacts(self):
        self.search_query = self.view.get_search_query()
        self.current_page = 1
        self.display_contacts()
    
    def display_about_info(self):
        about_info = """
        Contact Management App

        Description:
        This application allows you to manage your contacts.

        Creator: Swathik Devadiga
        Version: 1.0
        Last Modified: {}
        """.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        messagebox.showinfo("About", about_info)
    
    def on_double_click(self, event):
        item = self.view.contact_tree.selection()
        if item:
            contact_id = self.view.contact_tree.item(item, 'values')[0]
            if contact_id:
                contact = self.model.get_contact_by_id(contact_id)
                if contact:
                    # Preenche o formulário com os dados do contato
                    self.view.clear_form()
                    self.view.name_entry.insert(0, contact[1])
                    self.view.phone_entry.insert(0, contact[2])
                    self.view.email_entry.insert(0, contact[3])
                    self.view.address_entry.insert(0, contact[4])
    
    def contact_tree_popup(self, event):
        item = self.view.contact_tree.identify_row(event.y)
        if item:
            contact_id = self.view.contact_tree.item(item, 'values')[0]
            popup_menu = tk.Menu(self.view.root, tearoff=0)
            popup_menu.add_command(
                label="Edit Contact", 
                command=lambda: self.on_double_click(event)
            )
            popup_menu.add_command(
                label="Delete Contact", 
                command=lambda: self.delete_contact(contact_id)
            )
            popup_menu.post(event.x_root, event.y_root)
    
    def close(self):
        self.model.close()