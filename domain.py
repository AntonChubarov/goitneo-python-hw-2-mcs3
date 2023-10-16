from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @staticmethod
    def is_valid_phone(value: str):
        return len(str(value)) == 10 and value.isdigit()


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone in self.phones:
            raise ValueError(f"{self.name} record has phone {phone}")

        self.phones.append(phone)

    def remove_phone(self, phone: str):
        phone = Phone(phone)
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        old_phone = Phone(old_phone)
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)
            return

        raise ValueError(
            f"phone {old_phone} wasn't found in record {self.name}")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phone_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("record must be an instance of the Record class")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        result = ""
        for record in self.data.values():
            result += str(record) + "\n"

        return result


if __name__ == "__main__":
    # task test script

    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
    
    # additional test script

    john_record.remove_phone("5555555555")
    print(john_record)

    try:
        john_record.add_phone("1112223333")
    except Exception as e:
        print(f"error: {e}")

    try:
        john_record.edit_phone("5555555555", "6666666666")
    except Exception as e:
        print(f"error: {e}")

    book.add_record(jane_record)
    jane_record.add_phone("0975554862")

    print(str(book))
