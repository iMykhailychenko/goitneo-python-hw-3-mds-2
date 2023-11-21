import unittest

from app.controller import controller
from app.models import AddressBook
from app.mock.contacts import get_contacts


class TestValidations(unittest.TestCase):
    def test_invalid_command(self):
        """Handle invalid command"""
        result = controller("test", AddressBook())
        self.assertEqual(result, "Invalid command.")

        contacts = get_contacts()
        result = controller("change Ivan 1234567890", contacts)
        self.assertEqual(result, "Invalid command.")

        result = controller("change Ivan", contacts)
        self.assertEqual(result, "Invalid command.")

    def test_invalid_phone(self):
        """Handle invalid command"""
        result = controller("add Ivan 12345678900", AddressBook())  # Long
        self.assertEqual(result, "Phone number must be 10 digits long.")

        result = controller("add Ivan A234567890", AddressBook())  # Test letter
        self.assertEqual(result, "Phone number must be 10 digits long.")

        result = controller("add Ivan 123456789", AddressBook())
        self.assertEqual(result, "Phone number must be 10 digits long.")  # Short

    def test_invalid_birthday(self):
        """
        Tests the functionality of adding and showing birthdays for contacts.
        """
        contacts = get_contacts()

        # Invalid month - 20
        result = controller("add-birthday Taras 10.20.2023", contacts)
        self.assertEqual(result, "Date of birth must be in DD.MM.YYYY format.")

        result = controller("show-birthday Taras", contacts)
        self.assertEqual(result, "-")
