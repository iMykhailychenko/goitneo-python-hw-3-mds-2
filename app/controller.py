from typing import Optional

from app.constants import BotCommands
from app.models import AddressBook
from app.services import (
    add_birthday,
    add_contact,
    birthdays,
    change_contact,
    get_all_contacts,
    get_contact,
    parse_input,
    show_birthday,
    delete_contact,
)
from app.validations import input_error

services_map = {
    BotCommands.ADD.value: add_contact,
    BotCommands.CHANGE.value: change_contact,
    BotCommands.PHONE.value: get_contact,
    BotCommands.ALL.value: get_all_contacts,
    BotCommands.ADD_BIRTHDAY.value: add_birthday,
    BotCommands.SHOW_BIRTHDAY.value: show_birthday,
    BotCommands.BIRTHDAYS.value: birthdays,
    BotCommands.DELETE.value: delete_contact,
    BotCommands.HELLO.value: lambda *_: "How can I help you?",
    BotCommands.EXIT.value: lambda *_: None,
    BotCommands.CLOSE.value: lambda *_: None,
}


@input_error
def controller(user_input: str, contacts: AddressBook) -> Optional[str]:
    cmd, *args = parse_input(user_input)

    return services_map.get(cmd, lambda *_: "Invalid command.")(contacts, args)
