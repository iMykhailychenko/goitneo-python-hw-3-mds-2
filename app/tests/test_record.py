import unittest

from app.models import Phone, Record


class TestRecord(unittest.TestCase):
    def test_add_phone(self):
        record = Record("Ivan")

        record.add_phone("1234567890")
        self.assertEqual(record.phones, {Phone("1234567890")})

        record.add_phone("0987654321")
        self.assertEqual(record.phones, {Phone("1234567890"), Phone("0987654321")})

    def test_remove_phone(self):
        record = Record("Ivan")
        record.add_phone("1234567890")
        record.add_phone("0987654321")

        self.assertEqual(record.phones, {Phone("1234567890"), Phone("0987654321")})

        record.remove_phone("0987654321")
        self.assertEqual(record.phones, {Phone("1234567890")})

    def test_edit_phone(self):
        record = Record("Ivan")
        record.add_phone("1234567890")

        record.edit_phone("1234567890", "0987654321")
        self.assertEqual(record.phones, {Phone("0987654321")})

    def test_find_phone(self):
        record = Record("Ivan")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        record.add_phone("1234111111")

        result = record.find_phone("123")
        self.assertTrue(Phone("1234567890") in result)
        self.assertTrue(Phone("1234111111") in result)
        self.assertFalse(Phone("0987654321") in result)

        result = record.find_phone("0987")
        self.assertFalse(Phone("1234567890") in result)
        self.assertFalse(Phone("1234111111") in result)
        self.assertTrue(Phone("0987654321") in result)
