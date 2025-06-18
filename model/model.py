import sqlite3
import csv
from math import ceil

class ContactModel:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT
            )
        ''')
        self.conn.commit()
    
    def add_contact(self, name, phone, email, address):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", 
            (name, phone, email, address)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def update_contact(self, contact_id, name, phone, email, address):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
            (name, phone, email, address, contact_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_contact(self, contact_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_contacts(self, offset, limit, search_query=None):
        cursor = self.conn.cursor()
        if search_query:
            cursor.execute(
                "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? LIMIT ? OFFSET ?", 
                (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', limit, offset)
            )
        else:
            cursor.execute(
                "SELECT * FROM contacts LIMIT ? OFFSET ?", 
                (limit, offset)
            )
        return cursor.fetchall()
    
    def get_contact_by_id(self, contact_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
        return cursor.fetchone()
    
    def count_contacts(self, search_query=None):
        cursor = self.conn.cursor()
        if search_query:
            cursor.execute(
                "SELECT COUNT(*) FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?", 
                (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM contacts")
        return cursor.fetchone()[0]
    
    def import_csv(self, file_path):
        try:
            with open(file_path, 'r', newline='') as csvfile:
                csvreader = csv.DictReader(csvfile)
                for row in csvreader:
                    self.add_contact(
                        row.get('Name', ''),
                        row.get('Phone', ''),
                        row.get('Email', ''),
                        row.get('Address', '')
                    )
            return True, "Contacts imported successfully from CSV."
        except Exception as e:
            return False, f"Error importing CSV: {str(e)}"
    
    def close(self):
        self.conn.close()