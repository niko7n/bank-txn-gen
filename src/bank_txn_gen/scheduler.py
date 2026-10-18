import random
from collections.abc import Iterator
from datetime import date, timedelta

from .models import Transaction
from .sources import Source


def days_iterator(start: date, end: date) -> Iterator[date]:
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def loop_days(
    start: date, end: date, sources: list[Source], rng: random.Random
) -> list[Transaction]:
    txn_list: list[Transaction] = []
    for day in days_iterator(start, end):
        for source in sources:
            txn_list.extend(source(day, rng))

    return txn_list
