import logging
import json
import numpy as np

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def evaluateSalad():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    numberOfSalads = data.get("number_of_salads")

    n = len(streetArray[0])
    currentSum = 0
    # bestStreet = None
    streetArray = data.get("salad_prices_street_map")

    if (n == numberOfSalads):  # When the number of salads required is the number of shops available, one X value will not give a result
        for street in streetArray:
            sumOnStreet = 0
            for i in street:
                try:
                    sumOnStreet += int(i)
                except:
                    break
                    print("This street does not have enough shops")
                if (i == n):
                    if (currentSum == 0 or sumOnStreet <= currentSum):
                        currentSum = sumOnStreet
    else:  # This case is when there are more salad shops than the required number
        for street in streetArray:
            sumOnStreet = 0
            consecutiveShops = 0
            for i in street:
                try:
                    consecutiveShops += 1
                    sumOnStreet += int(i)
                except:
                    sumOnStreet = 0
                    consecutiveShops = 0
                if (consecutiveShops == numberOfSalads):
                    currentSum = sumOnStreet
    result = currentSum
    logging.info("My result :{}".format(result))
    return json.dumps(result)
