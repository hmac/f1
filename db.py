""" Handles database interation """
import os
import psycopg2
import psycopg2.extras

CONNECTION = None
CURSOR = None


def conn():
    """ Returns a database connection """
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = psycopg2.connect(os.environ["DATABASE_URL"])
    return CONNECTION


def c():
    """ Returns a cursor for the current database connection """
    global CURSOR
    if CURSOR is None:
        CURSOR = conn().CURSOR()
    return CURSOR


def fetchall(query):
    """ Takes a SQL query, executes it and returns the result set """
    with conn().cursor() as curs:
        curs.execute(query)
        return curs.fetchall()


def migrate(migrations_directory):
    """ Migrate the DB to the latest version """
    c = conn()
    with c:
        migration_files = os.scandir(migrations_directory)
        migrations = set(
            [int(f.name.strip(".sql")) for f in migration_files]
        )
        with c.cursor() as curs:
            curs.execute("SELECT version FROM schema_migrations")
            existing = set([v for (v,) in curs.fetchall()])
        c.commit()
        for migration in sorted(list(migrations - existing)):
            print(f'Running migration {migration}')
            filename = f'{migrations_directory}/{migration}.sql'
            with c.cursor() as curs, open(filename) as sql_file:
                sql = sql_file.read()
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
            curs.execute(
                "INSERT INTO results values (%s, %s, %s, %s, %s)", values
            )
        conn().commit()


def driver_positions(driver, year=None):
    """ Returns all finishing positions for a driver, ever """
    with conn().cursor() as curs:
        query = ("SELECT position FROM results WHERE driver = %s", (driver,))
        if year:
            query = (
                "SELECT position FROM results WHERE driver = %s AND year = %s",
                (driver, year)
            )
        curs.execute(*query)
        positions = curs.fetchall()
        return [p[0] for p in positions]


def race_result(year, race):

    """Retrieves the results for a given race."""

    query = """SELECT results.position AS position, drivers.name AS driver,
                 teams.name AS team, results.points AS points
                   FROM results, drivers, teams
                     WHERE results.driver_id = drivers.id
                       AND results.team_id = teams.id
                       AND results.year = %s
                       AND round = %s"""

    with conn().cursor() as cur:

        cur.execute(query, (year, race))
        return cur.fetchall()


def drivers():

    """Retrieves all the drivers."""

    with conn().cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

        cur.execute('SELECT * FROM drivers')
        return cur.fetchall()


def teams():

    """Retrieves all the teams."""

    with conn().cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

        cur.execute('SELECT * FROM teams')
        return cur.fetchall()
