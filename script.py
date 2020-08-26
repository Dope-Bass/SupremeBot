from cSupremeBot import SupremeBot

PERF = 7
FIRS = 5

import time
KEY = 0
VALUE = 1
ELEMENT = 2
HOME = 'https://www.supremenewyork.com/shop/all'

def funcPerfectMatch(object):
    object.searchAll()

def funcFirstMatch(object):
    object.findFirstMatch({"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"},
                          "/sweatshirts", True)

items = {
        # "/jackets": [],
        # "/shirts": [],
        # "/tops_sweaters": [],
        "/sweatshirts": [{"name": "Portrait Hooded Sweatshirt", "color": "Royal", "size": "Large"}],
        # "/pants": [],
        # "/shorts": []
    }

obj = SupremeBot(items)

funcFirstMatch(obj)
# funcPerfectMatch(obj)