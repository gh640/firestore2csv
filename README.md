# `firestore2csv.py`

A Python script to dump Firestore collection data with CSV format.

## Requirements

- Python 3.9
- Poetry 1.x

## Usage

Clone this repo.

```bash
git clone https://github.com/gh640/firestore2csv.git
```

Install dependency packages with [Poetry](https://github.com/python-poetry/poetry).

```bash
cd firestore2csv
poetry install
```

Run the script.

```bash
poetry run python firestore2csv.py \
  --cred-file firebase-service-account.json \
  --collection-name mycollection \
  --fields field_a,field_b,field_c \
  --order-by field_c \
  --direction ASC
```

Available options (all required):

- `--cred-file`
- `--collection-name`
- `--fields`
- `--order-by`
- `--direction`
