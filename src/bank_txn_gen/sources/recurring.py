import random
from collections.abc import Callable
from datetime import date

from ..models import Transaction
from ..persona import Persona
from .base import Source, inflow, month_label, outflow

Purpose = Callable[[date, random.Random], str]


def make_monthly(
    persona: Persona,
    key: str,
    day_of_month: int,
    amount: str,
    purpose: Purpose,
    *,
    incoming: bool = False,
) -> Source:
    book = inflow if incoming else outflow

    def monthly(day: date, rng: random.Random) -> list[Transaction]:
        if day.day != day_of_month:
            return []
        return [book(day, persona, persona[key], amount, purpose(day, rng))]

    return monthly


def make_recurring(persona: Persona) -> list[Source]:
    return [
        make_monthly(
            persona,
            "landlord",
            28,
            "850.00",
            lambda d, _: f"Miete {month_label(d)} {d.year}",
        ),
        make_monthly(
            persona,
            "health-insurance",
            1,
            "452.85",
            lambda d, rng: f"TK-BuchNR {rng.randrange(12**12):012d} {month_label(d)}",
        ),
        make_monthly(
            persona,
            "pension-insurance",
            1,
            "100",
            lambda _, rng: f"{rng.randrange(5**5):05d}",
        ),
        make_monthly(
            persona,
            "employer",
            15,
            "2444.15",
            lambda d, _: f"Gehalt {month_label(d)} {d.year}",
            incoming=True,
        ),
        make_monthly(
            persona,
            "fitness-gym",
            1,
            "30",
            lambda d, _: f"Mitgliedsbeitrag {month_label(d)}",
        ),
        make_monthly(
            persona,
            "savings",
            1,
            "200",
            lambda d, _: f"Sparrate {month_label(d)}",
        ),
    ]
