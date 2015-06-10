import api
import db
import requests
import scoring


# Get a driver's price
print("Price for Hamilton:", scoring.price('hamilton'))
# Get a driver's points so far this season
print("Hamilton's points so far:", scoring.points('hamilton'))


def reset_db():
    db.create_db()
    # Fetch all the Ergast data
    for i in range(1950, 2016):
        resp = requests.get("http://ergast.com/api/f1/%s.json" % (i,)).json()
        rounds = int(resp["MRData"]["total"])
        for j in range(1, rounds+1):
            print(j, i)
            db.store_race_result(i, j, api.race_result(i, j))
