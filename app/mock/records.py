from app.models import Record


def get_records() -> list[Record]:
    record1 = Record("Ivan")
    record1.add_phone("1234567890")

    record2 = Record("Taras")
    record2.add_phone("0987654321")

    return [record1, record2]
