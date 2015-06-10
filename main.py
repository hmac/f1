import api
import db
import requests

# Get info for some more races
print("Results for Catalunya 2008:")
for r in api.race_result(2008, 4):
    print(r['driver'])

db.create_db()
# Fetch all the Ergast data
for i in range(1950, 2016):
    resp = requests.get("http://ergast.com/api/f1/%s.json" % (i,)).json()
    rounds = int(resp["MRData"]["total"])
    for j in range(1, rounds+1):
        print(j, i)
        db.store_race_result(i, j, api.race_result(i, j))
