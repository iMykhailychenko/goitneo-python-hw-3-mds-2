from app.models import AddressBook
from app.controller import controller
from app.utils.logger import logger


def main():
    contacts = AddressBook()

    while True:
        logger.info("\nEnter a command: ")
        user_input = input()

        result = controller(user_input, contacts)
        if result is None:
            logger.error("\nGood bye!")
            break
        logger.warning(result)


if __name__ == "__main__":
    main()
