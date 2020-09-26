import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def evaluateSalad():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    numberOfSalads = data.get("number_of_salads")
    streetArray = data.get("salad_prices_street_map")
    result = saladSpree(numberOfSalads, streetArray)
    logging.info("My result :{}".format(result))
    return json.dumps(result)


# def saladSpree(numberOfSalads, streetArray):
#     n = len(streetArray[0])
#     currentSum = 0
#     if (n == numberOfSalads):  # When the number of salads required is the number of shops available, one X value will not give a result
#         for street in streetArray:
#             sumOnStreet = 0
#             for i in street:
#                 try:
#                     sumOnStreet += int(i)
#                 except:
#                     break
#                     print("This street does not have enough shops")
#                 if (i == n):
#                     if (currentSum == 0 or sumOnStreet <= currentSum):
#                         currentSum = sumOnStreet
#     else:  # This case is when there are more salad shops than the required number
#         for street in streetArray:
#             sumOnStreet = 0
#             consecutiveShops = 0
#             for i in street:
#                 try:
#                     consecutiveShops += 1
#                     sumOnStreet += int(i)
#                 except:
#                     sumOnStreet = 0
#                     consecutiveShops = 0
#                 if (consecutiveShops == numberOfSalads):
#                     currentSum = sumOnStreet
#     return currentSum

def saladSpree(numberOfSalads, streetArray):
    n = len(streetArray[0])
    currentSum = 0
    for street in streetArray:
        i=0
        while i < n-numberOfSalads:
            if all([x.isnumeric() for x in street[i:i+numberOfSalads]]):
                sum_ = sum([int(x) for x in street[i:i+numberOfSalads]])
                i+=1
                if not currentSum:
                    currentSum = sum_
                else :
                    if sum_ < currentSum:
                        currentSum = sum_
            else:
                i += "".join(street[i:i+numberOfSalads]).rindex("X")
    return currentSum
