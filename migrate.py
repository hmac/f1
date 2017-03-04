""" Migrate the database to the latest version and dump the schema to file """
import subprocess
import db

if __name__ == "__main__":
    db.migrate("./db/migrations")
    dump = subprocess.check_output(
        "pg_dump --schema-only --no-owner --no-privileges f1", shell=True
    )
    with open("./db/structure.sql", mode="wb") as f:
        f.write(dump)
