from enum import Enum
import requests


class CarStatus(Enum):
    """ An enum representing the status of a car at the end of the race """
    finished = 1
    failure = 2
    accident = 3


def race_result(year, round):
    """ Return an ordered array representing the result of a race.
        Each element of the array has the form
        {
            driver: <driver name>::string,
            status: <finishing status>::CarStatus
        }
        The array is ordered by finishing order, first to last.
    """
    RACE_RESULT_URL = "http://ergast.com/api/f1/%s/%s/results.json"

    def extract_result(r):
        return {"driver": r["Driver"]["driverId"],
                "status": parse_status(r["status"])}

    def parse_status(s):
        if s == "Finished":
            return CarStatus.finished
        if s.startswith("+"):  # +1 Lap, +2 Laps etc
            return CarStatus.finished
        if s == "Accident":
            return CarStatus.accident
        return CarStatus.failure

    resp = requests.get(RACE_RESULT_URL % (year, round)).json()
    raw_results = resp["MRData"]["RaceTable"]["Races"][0]["Results"]
    results = [extract_result(r) for r in raw_results]
    return results
