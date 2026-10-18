from datetime import date
from decimal import Decimal


def amount_de(amount: Decimal) -> str:
    s = f"{amount:,.2f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def date_de(day: date) -> str:
    return day.strftime("%d.%m.%y")


# Let optional fields appear as "" instead of "None"
def text(value: str | None) -> str:
    return value or ""
