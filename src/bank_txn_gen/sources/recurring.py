import random
from datetime import date

from ..models import Transaction
from ..persona import Persona
from .base import Source, inflow, month_label, outflow


def make_rent(persona: Persona) -> Source:
    def rent(day: date, rng: random.Random) -> list[Transaction]:
        if day.day != 28:
            return []
        return [
            outflow(
                day,
                persona,
                persona["landlord"],
                "850.00",
                f"Miete {month_label(day)} {day.year}",
            )
        ]

    return rent


def make_insurance(persona: Persona) -> Source:
    def insurance(day: date, rng: random.Random) -> list[Transaction]:
        if day.day != 1:
            return []
        return [
            outflow(
                day,
                persona,
                persona["health-insurance"],
                "452.85",
                f"TK-BuchNR {rng.randrange(12**12):012d} {month_label(day)}",
            ),
            outflow(
                day,
                persona,
                persona["pension-insurance"],
                "452.85",
                f"{rng.randrange(5**5):05d}",
            ),
        ]

    return insurance


def make_income_employment(persona: Persona) -> Source:
    def employment(day: date, rng: random.Random) -> list[Transaction]:
        if day.day != 15:
            return []
        return [
            inflow(
                day,
                persona["employer"],
                persona,
                "2444.15",
                f"Gehalt {month_label(day)} {day.year}",
            )
        ]

    return employment
