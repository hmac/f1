""" Migrate the database to the latest version and dump the schema to file """
import subprocess
import db

if __name__ == "__main__":
    db.migrate("./db/migrations")
    dump = subprocess.check_output(
        "pg_dump --schema-only --no-owner --no-privileges f1", shell=True
    )
    schema_migrations = db.fetchall(
        "SELECT version FROM schema_migrations ORDER BY version ASC"
    )
    with open("./db/structure.sql", mode="wb") as f:
        f.write(dump)

        template = "INSERT INTO schema_migrations (version) VALUES (%s);\n"
        for migration in schema_migrations:
            f.write(str.encode(template % migration))
