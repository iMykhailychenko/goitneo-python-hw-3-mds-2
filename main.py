from app.models import AddressBook
from app.controller import controller
from app.utils.logger import logger
from db import Database


def main():
    contacts = AddressBook()

    db = Database()
    db.read(contacts)

    while True:
        logger.info("\nEnter a command: ")
        user_input = input()

        result = controller(user_input, contacts)
        if result is None:
            logger.error("\nGood bye!")
            db.save(contacts)
            break
        logger.warning(result)


if __name__ == "__main__":
    main()
