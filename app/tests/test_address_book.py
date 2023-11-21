import unittest

from app.models import Record, AddressBook


class TestAddressBook(unittest.TestCase):
    def test_add_contact(self):
        record = Record("Ivan")
        record.add_phone("1234567890")

        contact = AddressBook()
        contact.add_contact(record)

        self.assertEqual(
            str(contact), "Contact name: Ivan, phones: 1234567890, birthday: -"
        )

    def test_find_contact(self):
        record = Record("Ivan")
        record.add_phone("1234567890")

        contact = AddressBook()
        contact.add_contact(record)

        result = contact.find("Ivan")
        self.assertEqual(result, record)

    def test_delete_contact(self):
        record1 = Record("Ivan")
        record1.add_phone("1234567890")

        record2 = Record("Ivan2")
        record2.add_phone("1234567890")

        contact = AddressBook()
        contact.add_contact(record1)
        contact.add_contact(record2)

        contact.delete("Ivan")
        result = contact.find("Ivan")
        self.assertIsNone(result)
