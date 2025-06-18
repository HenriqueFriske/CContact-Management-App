from model.model import ContactModel
from view.view import ContactView
from validators.validators import ContactValidator
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
            'delete_contact': self.delete_selected_contact,
            'clear_form': self.clear_form,
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
        errors = ContactValidator.validate_contact(
            data['name'], 
            data['phone'], 
            data['email']
        )
        
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
            
        self.model.add_contact(
            data['name'], 
            data['phone'], 
            data['email'], 
            data['address']
        )
        self.view.clear_form()
        self.display_contacts()
        messagebox.showinfo("Success", "Contact added successfully.")
    
    def delete_selected_contact(self):
        contact_id = self.view.get_selected_contact_id()
        if contact_id:
            if messagebox.askyesno(
                "Confirm Delete", 
                "Are you sure you want to delete this contact?"
            ):
                success = self.model.delete_contact(contact_id)
                if success:
                    self.display_contacts()
                    messagebox.showinfo("Success", "Contact deleted successfully")
                else:
                    messagebox.showerror("Error", "Failed to delete contact.")
        else:
            messagebox.showerror("Error", "Please select a contact to delete.")
    
    def clear_form(self):
        self.view.clear_form()
    
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
            success, msg = self.model.export_csv(file_path)
            if success:
                messagebox.showinfo("Export Successful", msg)
            else:
                messagebox.showerror("Error", msg)
    
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
                command=lambda: self.delete_selected_contact()
            )
            popup_menu.post(event.x_root, event.y_root)
    
    def close(self):
        self.model.close()