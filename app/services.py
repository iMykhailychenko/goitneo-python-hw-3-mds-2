from datetime import date, datetime, timedelta

from app.models import AddressBook, Record


def parse_input(user_input: str) -> list[str]:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(contacts: AddressBook, args: list[str]) -> str:
    name, phone = args

    record = Record(name)
    record.add_phone(phone)

    contacts.add_contact(record)
    return "Contact added."


def change_contact(contacts: AddressBook, args: list[str]) -> str:
    name, old_phone, new_phone = args

    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        raise KeyError()


def get_contact(contacts: AddressBook, args: list[str]) -> str:
    contact = contacts.find(args[0])
    if not contact:
        return "Contact not found."
    return "; ".join(map(str, contact.phones))


def get_all_contacts(contacts: AddressBook, *args: list[str]) -> str:
    return str(contacts) or "No contacts available."


def add_birthday(contacts: AddressBook, args: list[str]) -> str:
    name, b_day = args
    record = contacts.find(name)

    if record:
        record.add_birthday(b_day)
        return "Birthday added."
    else:
        raise KeyError()


def show_birthday(contacts: AddressBook, args: list[str]) -> str:
    record = contacts.find(args[0])

    if record:
        return record.birthday.value if hasattr(record.birthday, "value") else "-"
    else:
        raise KeyError()


def delete_contact(contacts: AddressBook, args: list[str]) -> str:
    contacts.delete(args[0])


def change_birthday_to_this_year(birthday: date, year: int) -> date:
    """Changes year to current year and handles leap years exceptions"""
    try:
        return birthday.replace(year=year)
    except ValueError:
        return birthday.replace(year=year, day=(birthday.day - 1))


def format_birthdays_list(birthdays: dict[str, list[str]]) -> str:
    """
    Returns a string that contains the names and corresponding
    birthdays from the input dictionary.
    """
    result = ""
    for key, value in birthdays.items():
        result += f"{key}: {'; '.join(value)}\n"
    return result.strip()


def birthdays(contacts: AddressBook, *args: list[str]) -> str:
    today = datetime.today().date()
    birthday_map: dict[str, list[str]] = {}

    for record in contacts.data.values():
        if record.birthday:
            day, month, year = map(int, record.birthday.value.split("."))
            birthday = date(year=year, month=month, day=day)
            birthday_this_year = change_birthday_to_this_year(birthday, today.year)

            if today < birthday_this_year <= today + timedelta(days=7):
                weekday_name = birthday_this_year.strftime("%A")
                if weekday_name not in birthday_map:
                    birthday_map[weekday_name] = [str(record)]
                    continue
                birthday_map[weekday_name].append(str(record))

    return format_birthdays_list(birthday_map)
