# bank-txn-gen

Generate realistic fake bank transactions and export them as a bank statement CSV.

**Current State:**
Active development and missing the random daily outflow.

## Installation

Install dependencies using **uv**:

```bash
uv sync
```
    
## Usage/Examples

```bash
usage: bank-txn-gen [-h] [-f {german-dkb}] [-s SEED] [-o FILE] year

Generate a year of realistic fake bank transactions and export them as CSV.

positional arguments:
  year                  calendar year to generate transactions for

options:
  -h, --help            show this help message and exit
  -f, --format {german-dkb}
                        CSV layout of the target bank (default: german-dkb)
  -s, --seed SEED       random seed; the same seed always produces the same statement (default: 42)
  -o, --out FILE        output file (default: out/statement_<year>.csv) (default: None)

Example: bank-txn-gen 2026 --format german-dkb --seed 7
```

## Running Tests

To run tests, run the following command

```bash
  uv run pytest
```

