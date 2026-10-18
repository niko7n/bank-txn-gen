# Bank format definitions
from collections.abc import Callable
from dataclasses import dataclass, field

from ..models import Transaction
from .formatting import amount_de, date_de, text


@dataclass(frozen=True)
class Column:
    header: str
    value: Callable[[Transaction], str]


@dataclass(frozen=True)
class CsvFormat:
    name: str
    columns: list[Column]
    delimiter: str = ";"
    encoding: str = "utf-8-sig"
    preamble: list[list[str]] = field(
        default_factory=lambda: [[]] * 4
    )  # include 4 empty lines at the top


GERMAN_DEFAULT = CsvFormat(
    name="german-dkb",
    columns=[
        Column("Buchungsdatum", lambda t: date_de(t.booking_date)),
        Column("Wertstellung", lambda t: date_de(t.value_date or t.booking_date)),
        Column("Status", lambda t: t.state),
        Column("Zahlungspflichtige*r", lambda t: t.payer),
        Column("Zahlungsempfänger*in", lambda t: t.payee),
        Column("Verwendungszweck", lambda t: t.purpose),
        Column("Umsatztyp", lambda t: t.type),
        Column("IBAN", lambda t: t.iban),
        Column("Betrag (€)", lambda t: amount_de(t.amount)),
        Column("Gläubiger-ID", lambda t: text(t.creditor_ident)),
        Column("Mandatsreferenz", lambda t: text(t.mandate_ref)),
        Column("Kundenreferenz", lambda t: text(t.customer_ref)),
    ],
)

# TODO: Add name via cli argument
# Registry: name -> CsvFormat
FORMATS: dict[str, CsvFormat] = {
    GERMAN_DEFAULT.name: GERMAN_DEFAULT,
}
