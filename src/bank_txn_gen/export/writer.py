import csv
from collections.abc import Iterable
from pathlib import Path

from ..models import Transaction
from .formats import CsvFormat


def write_csv(path: Path, txn_list: Iterable[Transaction], fmt: CsvFormat) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding=fmt.encoding) as f:
        writer = csv.writer(f, delimiter=fmt.delimiter)

        writer.writerows(fmt.preamble)
        writer.writerow([c.header for c in fmt.columns])
        for t in txn_list:
            writer.writerow([c.value(t) for c in fmt.columns])
