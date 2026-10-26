import random
import tomllib
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
from pathlib import Path

from faker import Faker

from ..counterparty import Counterparty, generate_counterparty
from ..models import Transaction
from ..persona import Persona
from .base import Source, outflow


@dataclass(frozen=True)
class WeeklyRule:
    name: str
    min_per_week: int
    max_per_week: int
    weekday_weights: list[float]
    amount_mean: float
    amount_stddev: float
    amount_min: float
    purpose: str
    amount_max: float | None = None
    expected_per_week: float | None = None
    counterparty: str | None = None  # key into persona.counterparties
    name_patterns: list[str] | None = None  # Faker templates if no counterparty
    pool_size: int = 5

    def __post_init__(self) -> None:
        if len(self.weekday_weights) != 7:
            raise ValueError(
                f"[{self.name}] weekday_weights needs exactly 7 values (Mon..Sun)"
            )

        open_days = sum(1 for w in self.weekday_weights if w > 0)
        if not 0 <= self.min_per_week <= self.max_per_week <= open_days:
            raise ValueError(
                f"[{self.name}]"
                + "need 0 <= min_per_week <= max_per_week <= days with weight > 0"
            )

    @property
    def expected(self) -> float:
        if self.expected_per_week is None:
            return (self.min_per_week + self.max_per_week) / 2
        return self.expected_per_week


def load_semi_regular_config(path: Path | None = None) -> list[WeeklyRule]:
    if path is None:
        text = (files("bank_txn_gen") / "data" / "semi_regular.toml").read_bytes()
        data = tomllib.loads(text.decode("utf-8"))
    else:
        with open(path, "rb") as f:
            data = tomllib.load(f)

    rules: list[WeeklyRule] = []
    for i, entry in enumerate(data.get("weekly", [])):
        try:
            rules.append(WeeklyRule(**entry))
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"semi_regular config: weekly #{i} '{entry.get('name', '?')}': {e}"
            ) from e
    return rules


def counterparty_pool(
    persona: Persona, rule: WeeklyRule, fake: Faker, rng: random.Random
) -> list[Counterparty]:
    if rule.counterparty:
        return [persona[rule.counterparty]]

    patterns = rule.name_patterns or ["{{company}}"]
    return [generate_counterparty(patterns, fake, rng) for _ in range(rule.pool_size)]


def probability(rule: WeeklyRule, day: date, done: int) -> float:
    weight = rule.weekday_weights[day.weekday()]
    if weight <= 0 or done >= rule.max_per_week:
        return 0.0

    # Days left in this week (incl. today) on which the rule may still fire
    days_left = sum(1 for w in rule.weekday_weights[day.weekday() :] if w > 0)
    if rule.min_per_week - done >= days_left:
        return 1.0

    return min(1.0, rule.expected * weight / sum(rule.weekday_weights))


def random_amount(rule: WeeklyRule, rng: random.Random) -> str:
    value = max(rule.amount_min, rng.gauss(rule.amount_mean, rule.amount_stddev))
    if rule.amount_max is not None:
        value = min(value, rule.amount_max)
    return f"{value:.2f}"


def make_weekly(
    persona: Persona, rule: WeeklyRule, fake: Faker, rng: random.Random
) -> Source:
    pool = counterparty_pool(persona, rule, fake, rng)
    current_week: tuple[int, int] | None = None
    done = 0

    def weekly(day: date, rng: random.Random) -> list[Transaction]:
        nonlocal current_week, done
        week = (day.isocalendar().year, day.isocalendar().week)
        if week != current_week:
            current_week, done = week, 0

        if rng.random() >= probability(rule, day, done):
            return []

        done += 1
        return [
            outflow(
                day,
                persona,
                rng.choice(pool),
                random_amount(rule, rng),
                rule.purpose,
            )
        ]

    return weekly


def make_semi_regular(
    persona: Persona, seed: int, config_path: Path | None = None
) -> list[Source]:
    fake = Faker("de_DE")
    fake.seed_instance(seed)
    rng = random.Random(f"{seed}: semi_regular")
    return [
        make_weekly(persona, rule, fake, rng)
        for rule in load_semi_regular_config(config_path)
    ]
