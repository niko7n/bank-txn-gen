import argparse
import random
from datetime import date
from pathlib import Path

from .export import FORMATS, write_csv
from .models import Transaction
from .persona import Persona, make_persona
from .scheduler import loop_days
from .sources import (
    Source,
    make_income_employment,
    make_insurance,
    make_rent,
    make_semi_regular,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bank-txn-gen",
        description=(
            "Generate a year of realistic fake bank transactions "
            "and export them as CSV."
        ),
        epilog="Example: bank-txn-gen 2026 --format german-dkb --seed 7",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "year",
        type=int,
        help="calendar year to generate transactions for",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=sorted(FORMATS),
        default="german-dkb",
        help="CSV layout of the target bank",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=42,
        help="random seed; the same seed always produces the same statement",
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        metavar="FILE",
        help="output file (default: out/statement_<year>.csv)",
    )
    return parser


def build_sources(persona: Persona, seed: int) -> list[Source]:
    return [
        make_rent(persona),
        make_insurance(persona),
        make_income_employment(persona),
        *make_semi_regular(persona, seed),
    ]


def generate(year: int, seed: int) -> list[Transaction]:
    rng = random.Random(seed)
    persona = make_persona(seed)
    sources = build_sources(persona, seed)
    return loop_days(date(year, 1, 1), date(year, 12, 31), sources, rng)


def main() -> None:
    args = build_parser().parse_args()

    out = args.out or Path(f"out/statement_{args.year}.csv")
    txns = generate(args.year, args.seed)
    write_csv(out, txns, FORMATS[args.format])

    print(f"Wrote {len(txns)} fake transactions to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
