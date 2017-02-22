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


# ----- Routes ----- #

@app.route('/2014')
def index():

	query = 'SELECT * FROM results where year > 2014'
	results = db.fetchall(query)
	races = split_races(results)

	return render_template('index.html', races=races)


@app.route('/prices')
def prices():

	query = 'SELECT DISTINCT driver FROM results WHERE year = 2014'
	drivers = db.fetchall(query)
	driver_prices = [(d[0], scoring.price(d[0])) for d in drivers]

	return render_template('prices.html', prices=driver_prices)
