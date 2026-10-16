import random
from datetime import date
from decimal import Decimal

from ..models import Transaction


def rent(day: date, rng: random.Random) -> list[Transaction]:
    if day.day != 28:
        return []
    return [
        # TODO: Add Faker
        Transaction(
            booking_date=day,
            value_date=day,
            state="Gebucht",
            payee="Hausverwaltung Beispiel GmbH",
            payer="Max Mustermann",
            purpose="Miete",
            type="Ausgang",
            iban="DE89370400440532013000",
            # TODO: placeholder, persona.py replaces this
            amount=Decimal("-850.00"),
        )
    ]
