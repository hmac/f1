import sqlite3

DB_PATH = "db.sqlite"
connection = None
cursor = None


def conn():
    global connection
    if connection is None:
        connection = sqlite3.connect(DB_PATH)
    return connection


def c():
    global cursor
    if cursor is None:
        cursor = conn().cursor()
    return cursor


def create_db():
    """ Create the database tables. We will need tables for F1 standings,
        race results, users, and probably other things I've forgotten """
    c().execute("DROP TABLE IF EXISTS results")
    c().execute("CREATE TABLE results (driver TEXT, year INTEGER, round INTEGER, position INTEGER, status INTEGER)")
    conn().commit()


def store_race_result(year, round, result):
    """ Stores a race result in the database """
    for r in result:
        position = result.index(r)+1
        values = (r['driver'], year, round, position, r['status'].value)
        c().execute("INSERT INTO results values (?,?,?,?,?)", values)
    conn().commit()


def driver_positions(driver, year=None):
    """ Returns all finishing positions for a driver, ever """
    if year:
        query = ("SELECT position FROM results WHERE driver=? AND year=?", (driver, year))
    else:
        query - ("SELECT position FROM results WHERE driver=?", (driver,))
    positions = c().execute(*query).fetchall()
    return [p[0] for p in positions]


