# This module will implement scoring for each driver based on their past race
# performance
import db
from math import floor

POINTS = [0, 25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


def price_multiplier(driver):
    """ Sum the total lifetime points of the driver """
    positions = db.driver_positions(driver)
    return sum([POINTS[p] for p in positions if p < 11])


def price(driver):
    """ Returns the price of the driver in millions """
    return floor(10 + 0.05*price_multiplier(driver))


def points(driver):
    """ Returns the total points a driver has been awarded this season """
    # TODO: replace hardcoded year
    positions = db.driver_positions(driver, 2015)
    return sum([POINTS[p] for p in positions if p < 11])
