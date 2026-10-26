import random
import tomllib
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path

from faker import Faker

# BLZ
BANK_CODES = ["37040044", "10010010", "50010517", "12030000", "70150000", "10070024"]


@dataclass
class Counterparty:
    name: str
    iban: str
    creditor_ident: str | None = None


def load_counterparty_config(path: Path | None = None) -> dict[str, dict]:
    if path is None:
        text = (files("bank_txn_gen") / "data" / "counterparties.toml").read_bytes()
        data = tomllib.loads(text.decode("utf-8"))
    else:
        with open(path, "rb") as f:
            data = tomllib.load(f)

    for key, entry in data.items():
        if ("name" in entry) == ("name_patterns" in entry):
            raise ValueError(
                f"counterparties config: '{key}' needs exactly one of "
                "'name' or 'name_patterns'"
            )

    return data


def make_iban(rng: random.Random) -> str:
    bban = rng.choice(BANK_CODES) + f"{rng.randrange(10**10):010d}"
    check = 98 - int(bban + "131400") % 97  # "DE" -> 1314, check digits -> 00
    return f"DE{check:02d}{bban}"


def make_creditor_id(rng: random.Random) -> str:
    return f"DE{rng.randrange(10, 99)}{rng.randrange(10**11):011d}"


def generate_counterparty(
    patterns: list[str], fake: Faker, rng: random.Random
) -> Counterparty:
    return Counterparty(name=fake.parse(rng.choice(patterns)), iban=make_iban(rng))
