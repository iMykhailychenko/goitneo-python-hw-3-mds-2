from enum import Enum


class BotCommands(Enum):
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    DELETE = "delete"
    HELLO = "hello"
    EXIT = "exit"
    CLOSE = "close"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"


class InvalidNameError(Exception):
    ...


class InvalidPhoneError(Exception):
    ...


class InvalidBirthdayError(Exception):
    ...
