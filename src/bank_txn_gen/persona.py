import random
import tomllib
from dataclasses import dataclass, field
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


@dataclass
class Persona:
    name: str
    iban: str
    counterparties: dict[str, Counterparty] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Counterparty:
        return self.counterparties[key]


def load_counterparty_config(path: Path | None = None) -> dict[str, dict]:
    if path is None:
        text = (files("bank_txn_gen") / "data" / "counterparties.toml").read_bytes()
        data = tomllib.loads(text.decode("utf-8"))
    else:
        with open(path, "rb") as f:
            data = tomllib.load(f)

    for key, entry in data.items():
        missing = {"name"} - entry.keys()
        if missing:
            raise ValueError(
                f"counterparties config: '{key}' is missing {sorted(missing)}"
            )

    return data


def make_iban(rng: random.Random) -> str:
    bban = rng.choice(BANK_CODES) + f"{rng.randrange(10**10):010d}"
    check = 98 - int(bban + "131400") % 97  # "DE" -> 1314, check digits -> 00
    return f"DE{check:02d}{bban}"


def make_creditor_id(rng: random.Random) -> str:
    return f"DE{rng.randrange(10, 99)}ZZZ{rng.randrange(10**11):011d}"


def make_persona(seed: int, config_path: Path | None = None) -> Persona:
    rng = random.Random(seed)
    fake = Faker("de_DE")
    fake.seed_instance(seed)

    persona = Persona(name=fake.name(), iban=make_iban(rng))

    # TODO: Check why these are still not part of the config
    # Generated counterparties
    persona.counterparties["landlord"] = Counterparty(
        name=f"Hausverwaltung {fake.last_name()} GmbH", iban=make_iban(rng)
    )
    persona.counterparties["employer"] = Counterparty(
        name=fake.company(), iban=make_iban(rng)
    )

    # Config file counterparties with fixed iban
    for key, entry in load_counterparty_config(config_path).items():
        cp_rng = random.Random(f"{seed}:{key}")
        persona.counterparties[key] = Counterparty(
            name=entry["name"],
            iban=entry.get("iban") or make_iban(cp_rng),
            creditor_ident=entry.get("creditor_ident") or make_creditor_id(cp_rng),
        )
    return persona
