import unittest
from datetime import date
from unittest.mock import patch

from app.controller import controller
from app.models import AddressBook, Name, Phone, Record
from app.mock.contacts import get_contacts
from app.mock.records import get_records


class TestController(unittest.TestCase):
    mock_date = date(2023, 6, 6)  # mock date (Tuesday)

    def test_exit_command(self):
        """Returns None for exit or close commands"""
        result = controller("exit", AddressBook())
        self.assertIsNone(result)

        result = controller("close", AddressBook())
        self.assertIsNone(result)

    def test_case_insensitive(self):
        """Handle 'Hello' command in case insensitive manner"""
        result = controller("Hello", AddressBook())
        self.assertEqual(result, "How can I help you?")

        result = controller("HeLLo", AddressBook())
        self.assertEqual(result, "How can I help you?")

        result = controller("hello", AddressBook())
        self.assertEqual(result, "How can I help you?")

    def test_add_command(self):
        """Handle 'add' command"""
        contacts = AddressBook()

        result = controller("add Ivan 1234567890", contacts)
        phones = contacts.data[Name("Ivan")].phones

        self.assertEqual(result, "Contact added.")
        self.assertEqual(phones, {Phone("1234567890")})

        # Test case with second phone number
        result = controller("add Ivan 0987654321", contacts)
        self.assertEqual(result, "Contact added.")
        self.assertEqual(phones, {Phone("1234567890"), Phone("0987654321")})

    def test_change_command(self):
        """Handle 'change' command"""
        contacts = get_contacts()

        # Test if original phone is exist
        phones = contacts.data[Name("Ivan")].phones
        self.assertEqual(phones, {Phone("1234567890")})

        result = controller("change Ivan 1234567890 4321954783", contacts)

        # Test if original phone was changed
        self.assertEqual(result, "Contact changed.")
        self.assertEqual(phones, {Phone("4321954783")})

        # Test case for changing non-existent contact
        result = controller("change John 9876543210 1234567890", contacts)
        self.assertEqual(result, "User do not exist.")  # Ensure no changes

    def test_get_contact(self):
        """Handle 'phone' command"""
        record1, record2 = get_records()

        contacts = AddressBook()
        contacts.add_contact(record1)
        contacts.add_contact(record2)

        result = controller("phone Taras", contacts)
        self.assertEqual(result, "0987654321")

        # Show multiple phones
        record2.add_phone("1111111111")
        result = controller("phone Taras", contacts)
        self.assertTrue("1111111111" in result)
        self.assertTrue("0987654321" in result)

        # Test case for non-existent contact
        result = controller("phone John", contacts)
        self.assertEqual(result, "Contact not found.")

    def test_get_all_contact(self):
        """Handle 'all' command"""
        contacts = get_contacts()

        result = controller("all", contacts)
        self.assertEqual(
            result,
            "Contact name: Ivan, phones: 1234567890, birthday: -\nContact name: Taras, phones: 0987654321, birthday: -",
        )

        # Test case for empty contacts
        result = controller("all", AddressBook())
        self.assertEqual(result, "No contacts available.")

    def test_get_user_birthday(self):
        """
        Tests the functionality of adding and showing birthdays for contacts.
        """
        contacts = get_contacts()

        result = controller("add-birthday Ivan 20.10.2023", contacts)
        self.assertEqual(result, "Birthday added.")

        result = controller("show-birthday Ivan", contacts)
        self.assertEqual(result, "20.10.2023")

    @patch("app.services.datetime")
    def test_birthdays_this_week(self, mock_date):
        """Returns records with birthdays in upcoming week"""

        mock_date.today.return_value.date.return_value = self.mock_date

        record1, record2 = get_records()
        record1.add_birthday("07.06.2023")  # Should be shown
        record2.add_birthday("01.01.2023")  # Should be hidden

        contacts = AddressBook()
        contacts.add_contact(record1)
        contacts.add_contact(record2)

        result = controller("birthdays", contacts)
        self.assertEqual(
            result,
            "Wednesday: Contact name: Ivan, phones: 1234567890, birthday: 07.06.2023",
        )

    @patch("app.services.datetime")
    def test_birthdays_in_leap_year(self, mock_date):
        """Handles leap years properly"""

        mock_date.today.return_value.date.return_value = self.mock_date

        record1, record2 = get_records()
        record1.add_birthday("07.06.1992")  # Leap year
        record2.add_birthday("08.06.2001")  # Not leap year

        contacts = AddressBook()
        contacts.add_contact(record1)
        contacts.add_contact(record2)

        result = controller("birthdays", contacts)
        self.assertEqual(
            result,
            "Wednesday: Contact name: Ivan, phones: 1234567890, birthday: 07.06.1992\n"
            "Thursday: Contact name: Taras, phones: 0987654321, birthday: 08.06.2001",
        )

    @patch("app.services.datetime")
    def test_multiple_birthdays(self, mock_date):
        """Returns records with birthdays in upcoming week"""

        mock_date.today.return_value.date.return_value = self.mock_date

        record1, record2 = get_records()
        record1.add_birthday("07.06.2023")
        record2.add_birthday("07.06.2023")

        contacts = AddressBook()
        contacts.add_contact(record1)
        contacts.add_contact(record2)

        result = controller("birthdays", contacts)
        self.assertEqual(
            result,
            "Wednesday: Contact name: Ivan, phones: 1234567890, birthday: 07.06.2023; "
            "Contact name: Taras, phones: 0987654321, birthday: 07.06.2023",
        )

        record2.add_birthday("08.06.2023")
        result = controller("birthdays", contacts)
        self.assertEqual(
            result,
            "Wednesday: Contact name: Ivan, phones: 1234567890, birthday: 07.06.2023"
            "\nThursday: Contact name: Taras, phones: 0987654321, birthday: 08.06.2023",
        )
