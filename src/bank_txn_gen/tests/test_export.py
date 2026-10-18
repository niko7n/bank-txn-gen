from datetime import date
from decimal import Decimal

from bank_txn_gen.export import FORMATS, write_csv
from bank_txn_gen.models import Transaction


def test_german_export(tmp_path):
    t = Transaction(
        booking_date=date(2026, 10, 28),
        state="Gebucht",
        payee="Vermieter",
        payer="Max",
        purpose="Miete Oktober 2026",
        type="Ausgang",
        iban="DE02100100100006820101",
        amount=Decimal("-850.00"),
    )
    out = tmp_path / "test.csv"
    write_csv(out, [t], FORMATS["german-dkb"])

    lines = out.read_text(encoding="utf-8-sig").splitlines()
    assert lines[:4] == [""] * 4
    assert lines[4].startswith("Buchungsdatum;Wertstellung")
    assert "-850,00" in lines[5]
