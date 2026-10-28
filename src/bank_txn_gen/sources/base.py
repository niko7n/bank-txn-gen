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


def _booking(
    day: date,
    persona: Persona,
    cp: Counterparty,
    amount: str,
    purpose: str,
    *,
    incoming: bool,
    **extra,
) -> Transaction:
    value = abs(Decimal(amount))
    payer, payee = (cp.name, persona.name) if incoming else (persona.name, cp.name)

    return Transaction(
        booking_date=day,
        value_date=day,
        state="Gebucht",
        payer=payer,
        payee=payee,
        iban=cp.iban,
        amount=value if incoming else -value,
        purpose=purpose,
        type="Eingang" if incoming else "Ausgang",
        **extra,
    )


def outflow(
    day: date, persona: Persona, cp: Counterparty, amount: str, purpose: str, **extra
) -> Transaction:
    return _booking(day, persona, cp, amount, purpose, incoming=False, **extra)


def inflow(
    day: date, persona: Persona, cp: Counterparty, amount: str, purpose: str, **extra
) -> Transaction:
    return _booking(day, persona, cp, amount, purpose, incoming=True, **extra)
