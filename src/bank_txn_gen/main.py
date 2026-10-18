import random
from datetime import date
from pathlib import Path

from .export import FORMATS, write_csv
from .persona import make_persona
from .scheduler import loop_days
from .sources import make_income_employment, make_insurance, make_rent

SEED = 42


def main() -> None:
    rng = random.Random(SEED)
    year = 2026

    persona = make_persona(SEED)
    sources = [
        make_rent(persona),
        make_insurance(persona),
        make_income_employment(persona),
    ]
    txn_list = loop_days(date(year, 1, 1), date(year, 12, 31), sources, rng)

    # for t in txn_list:
    #    print(t.booking_date, t.amount, t.iban, t.payee, t.purpose, t.type, t.payer)

    write_csv(Path(f"out/statement_{year}.csv"), txn_list, FORMATS["german-dkb"])
