from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Transaction:
    booking_date: date
    state: str
    payee: str
    payer: str
    purpose: str
    type: str
    iban: str
    amount: Decimal  # negative = outflow
    value_date: date | None = None
    creditor_ident: str | None = None
    mandate_ref: str | None = None
    customer_ref: str | None = None
