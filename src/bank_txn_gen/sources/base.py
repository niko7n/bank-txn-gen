import random
from collections.abc import Callable
from datetime import date
from decimal import Decimal

from ..counterparty import Counterparty
from ..models import Transaction
from ..persona import Persona

Source = Callable[[date, random.Random], list[Transaction]]

MONTH_DE = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
]


def month_label(day: date) -> str:
    return f"{MONTH_DE[day.month - 1]}"


# TODO: Purpose could go into the toml
def outflow(
    day: date,
    persona: Persona,
    cp: Counterparty,
    amount: str,
    purpose: str,
    **extra,
) -> Transaction:
    return Transaction(
        booking_date=day,
        value_date=day,
        state="Gebucht",
        payer=persona.name,
        payee=cp.name,
        iban=cp.iban,
        amount=-abs(Decimal(amount)),
        purpose=purpose,
        type="Ausgang",
        **extra,
    )


def inflow(
    day: date,
    cp: Counterparty,
    persona: Persona,
    amount: str,
    purpose: str,
    **extra,
) -> Transaction:
    return Transaction(
        booking_date=day,
        value_date=day,
        state="Gebucht",
        payer=cp.name,
        payee=persona.name,
        iban=cp.iban,
        amount=abs(Decimal(amount)),
        purpose=purpose,
        type="Eingang",
        **extra,
    )
