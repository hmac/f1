# F1

[![CircleCI](https://circleci.com/gh/hmac/f1.svg?style=svg)](https://circleci.com/gh/hmac/f1)

## Install

Ideally set up a [virtual environment](https://docs.python.org/3/library/venv.html), and then run:

```
pip install -r requirements.txt
```

## Setup the database

1. Install [PostgreSQL](https://www.postgresql.org)
2. `createdb f1`
3. `echo "CREATE TABLE schema_migrations (version integer NOT NULL);" | psql f1`
4. [optional] Install [autoenv](https://github.com/kennethreitz/autoenv) and `echo "DATABASE_URL=postgres://localhost:5432/f1" > .env`

## Run

Run database migrations:

```
python migrate.py
```

Start the server:

```
gunicorn views:app
```
