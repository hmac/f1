import psycopg2
import os

DB_PATH = "db.sqlite"
connection = None
cursor = None


def conn():
    global connection
    if connection is None:
        connection = psycopg2.connect(os.environ["DATABASE_URL"])
    return connection


def c():
    global cursor
    if cursor is None:
        cursor = conn().cursor()
    return cursor


def fetchall(query):
    with conn().cursor() as curs:
        curs.execute(query)
        return curs.fetchall()


def migrate():
    """ Migrate the DB to the latest version """
    c = conn()
    with c:
        migrations = set(
            [int(f.name.strip(".sql")) for f in os.scandir("./migrations")]
        )
        with c.cursor() as curs:
            curs.execute("SELECT version FROM schema_migrations")
            existing = set([v for (v,) in curs.fetchall()])
        c.commit()
        for migration in sorted(list(migrations - existing)):
            with c.cursor() as curs:
                print("Running migration %s" % migration)
                sql = open("./migrations/%s.sql" % migration).read()
                print(sql)
                curs.execute(sql)
                curs.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    ([migration])
                )


def store_race_result(year, round, result):
    """ Stores a race result in the database """
    with conn().cursor() as curs:
        for r in result:
            position = result.index(r)+1
            values = (r['driver'], year, round, position, r['status'].value)
            curs.execute("INSERT INTO results values (%s, %s, %s, %s, %s)", values)
        conn().commit()


def driver_positions(driver, year=None):
    """ Returns all finishing positions for a driver, ever """
    with conn().cursor() as curs:
        query = ("SELECT position FROM results WHERE driver = %s", (driver,))
        if year:
            query = ("SELECT position FROM results WHERE driver = %s AND year = %s", (driver, year))
        curs.execute(*query)
        positions = curs.fetchall()
        return [p[0] for p in positions]


