# ----- Imports ----- #

import os
import sqlite3 as sql
import bottle
from bottle import Bottle, view, static_file, run


# ----- Setup ----- #

DB_PATH = "db.sqlite"
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_PATH = CURRENT_DIR + '/site/static'

app = Bottle()
bottle.TEMPLATE_PATH.insert(0, CURRENT_DIR + '/site/views')

conn = sql.connect(DB_PATH)


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

@app.route('/')
@view('index.html')
def index():

	results = []

	with conn:

		cursor = conn.cursor()
		cursor.execute('SELECT * FROM results where year > 2014')
		results = cursor.fetchall()

	races = split_races(results)

	return dict(races=races)


@app.route('/static/<filepath:path>')
def load_static(filepath):

	return static_file(filepath, root=STATIC_PATH)


# ----- Run ----- #

if __name__ == '__main__':

	run(app, host='localhost', port=8080)
