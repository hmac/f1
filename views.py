# ----- Imports ----- #

from flask import Flask, render_template

import db
import scoring


# ----- Setup ----- #

app = Flask(__name__, static_url_path='/static')


# ----- Functions ----- #

def split_races(results):

    races = []

    for x in range(1, 8):

        race = []

        for result in results:
            if result[2] is x:
                race.append(result)

        races.append(race)

    return races


def get_users():

    """Retrieves a list of users from the db."""

    # Dummy data for now.
    return [
        {'name': 'Dummy One', 'id': 1, 'points': 40},
        {'name': 'Dummy Two', 'id': 2, 'points': 34},
        {'name': 'Dummy Three', 'id': 3, 'points': 63}
    ];


# ----- Routes ----- #

@app.route('/')
def index():

    users = get_users()

    return render_template('index.html', users=users)


@app.route('/prices')
def prices():

    query = 'SELECT DISTINCT driver FROM results WHERE year = 2014'
    drivers = db.fetchall(query)
    driver_prices = [(d[0], scoring.price(d[0])) for d in drivers]

    return render_template('prices.html', prices=driver_prices)
