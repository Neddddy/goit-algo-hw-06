from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(self.validate(value))  

    @staticmethod
    def validate(value):
        if not re.fullmatch(r"^\d{10}$", value):
            raise ValueError("Invalid phone number format")
        return value  

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)

    def edit_phone(self, phone0, phone1):
        phone_obj = self.find_phone(phone0)
        if phone_obj:
            new_phone = Phone(phone1)  
            self.remove_phone(phone0)
            self.phones.append(new_phone)
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

print(book)

john = book.find("John")
if john:
    try:
        john.edit_phone("1234567890", "1112223333")  
        print(john)  
    except ValueError as e:
        print(e)

found_phone = john.find_phone("5555555555")
if found_phone:
    print(f"{john.name}: {found_phone.value}")

book.delete("Jane")
print(book)