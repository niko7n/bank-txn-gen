import random
from datetime import date

from .scheduler import loop_days
from .sources.recurring import rent


def main() -> None:
    rng = random.Random(42)
    year = 2026
    sources = [rent]
    txn_list = loop_days(date(year, 1, 1), date(year, 12, 31), sources, rng)

    for t in txn_list:
        print(t.booking_date, t.amount, t.payee)
