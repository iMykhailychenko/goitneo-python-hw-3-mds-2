import os
import csv

from pathlib import Path
from app.models import AddressBook, Record


class Database:
    __path = Path(".", "assets", "database.csv")

    def read(self, contacts: AddressBook) -> AddressBook:
        try:
            if not Database.__path.exists():
                return AddressBook()

            with open(Database.__path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record = Record(row["name"])

                    for i in row["phones"].split("|"):
                        record.add_phone(i)

                    if row["birthday"] != "None":
                        record.add_birthday(row["birthday"])

                    contacts.add_contact(record)
        except:
            print("Invalid data stored in database.csv")
            return AddressBook()

    def save(self, contacts: AddressBook) -> AddressBook:
        if not contacts.data:
            return

        if not Database.__path.exists():
            os.mkdir("assets")

        with open(Database.__path, "w+") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "phones", "birthday"])
            writer.writeheader()

            for record in contacts.data.values():
                phones = "|".join(map(str, record.phones))
                writer.writerow(
                    {
                        "phones": phones,
                        "name": record.name.value,
                        "birthday": str(record.birthday),
                    }
                )
