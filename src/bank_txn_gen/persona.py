import random
from dataclasses import dataclass, field
from pathlib import Path

from faker import Faker

from .counterparty import (
    Counterparty,
    generate_counterparty,
    load_counterparty_config,
    make_creditor_id,
    make_iban,
)


@dataclass
class Persona:
    name: str
    iban: str
    counterparties: dict[str, Counterparty] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Counterparty:
        return self.counterparties[key]


def make_persona(seed: int, config_path: Path | None = None) -> Persona:
    rng = random.Random(seed)
    fake = Faker("de_DE")
    fake.seed_instance(seed)

    persona = Persona(name=fake.name(), iban=make_iban(rng))

    # Config file counterparties with fixed iban
    for key, entry in load_counterparty_config(config_path).items():
        cp_rng = random.Random(f"{seed}:{key}")
        fake.seed_instance(f"{seed}:{key}")

        if "name_patterns" in entry:
            cp = generate_counterparty(entry["name_patterns"], fake, cp_rng)
        else:
            cp = Counterparty(name=entry["name"], iban=make_iban(cp_rng))

        cp.iban = entry.get("iban") or cp.iban
        cp.creditor_ident = entry.get("creditor_ident") or make_creditor_id(cp_rng)

        persona.counterparties[key] = cp
    return persona
