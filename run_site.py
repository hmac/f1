# ----- Imports ----- #

import os
import db
import scoring
import bottle
from bottle import Bottle, view, static_file, run


# ----- Setup ----- #

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = CURRENT_DIR + '/site/static'

app = Bottle()
bottle.TEMPLATE_PATH.insert(0, CURRENT_DIR + '/site/views')



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
@view('index.html')
def index():
	query = 'SELECT * FROM results where year > 2014'
	results = db.c().execute(query).fetchall()
	races = split_races(results)

	return dict(races=races)

@app.route('/prices')
@view('prices.html')
def prices():
	query = 'SELECT DISTINCT driver FROM results WHERE year = 2014'
	drivers = db.c().execute(query).fetchall()
	driver_prices = [(d[0], scoring.price(d[0])) for d in drivers]
	return dict(prices=driver_prices)

@app.route('/static/<filepath:path>')
def load_static(filepath):

	return static_file(filepath, root=STATIC_PATH)


# ----- Run ----- #

if __name__ == '__main__':

	run(app, host='localhost', port=8080)
