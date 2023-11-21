from app.models import AddressBook
from app.mock.records import get_records


def get_contacts():
    contacts = AddressBook()

    for record in get_records():
        contacts.add_contact(record)

    return contacts
