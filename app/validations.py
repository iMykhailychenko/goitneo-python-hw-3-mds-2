from functools import wraps

from app.constants import InvalidBirthdayError, InvalidNameError, InvalidPhoneError


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid command."
        except KeyError:
            return "User do not exist."
        except IndexError:
            return "Give me name and phone please."
        except InvalidPhoneError:
            return "Phone number must be 10 digits long."
        except InvalidNameError:
            return "Invalid name."
        except InvalidBirthdayError:
            return "Date of birth must be in DD.MM.YYYY format."
        except:
            return "Invalid command."

    return inner
