import re

class ContactValidator:
    @staticmethod
    def validate_contact(name, phone, email):
        errors = []
        
        # Name validation
        if not name.strip():
            errors.append("Name is required")
        elif len(name) > 100:
            errors.append("Name is too long (max 100 characters)")
        
        # At least one of phone or email is required
        if not phone.strip() and not email.strip():
            errors.append("At least one of Phone or Email is required")
        
        # Phone validation
        if phone.strip():
            # Remove non-digit characters
            cleaned_phone = re.sub(r'\D', '', phone)
            if not cleaned_phone:
                errors.append("Invalid phone number format")
            elif len(cleaned_phone) < 7 or len(cleaned_phone) > 15:
                errors.append("Phone number must be between 7-15 digits")
        
        # Email validation
        if email.strip():
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                errors.append("Invalid email format")
            elif len(email) > 100:
                errors.append("Email is too long (max 100 characters)")
        
        return errors