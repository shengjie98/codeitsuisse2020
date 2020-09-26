
import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])
def evaluate_portfolio():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data.get("inputs")
    outputs = [getOutput(input_dict) for input_dict in inputs]
    result = {"outputs": outputs}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def getOutput(input_dict):
    bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["CoRelationCoefficient"])
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["FuturePrcVol"])
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: math.sqrt(input_dict["Portfolio"]["SpotPrcVol"]**2 + x["FuturePrcVol"]**2 + 2 *x["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] *x["FuturePrcVol"]))
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x["FuturePrcVol"])
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x["FuturePrcVol"] / x["Notional"] * input_dict["Portfolio"]["Value"] / x["IndexFuturePrice"] )
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["Notional"] * input_dict["Portfolio"]["Value"] / x["IndexFuturePrice"] )
    # bestIndex = max(input_dict["IndexFutures"], key = lambda x: x["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x["FuturePrcVol"])
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["CoRelationCoefficient"] * x["FuturePrcVol"] )
    # print(bestIndex)
    # print(input_dict["IndexFutures"])
    output = {"HedgePositionName": bestIndex["Name"]}
    optimalHedgeRatio = bestIndex["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / bestIndex["FuturePrcVol"]
    num = optimalHedgeRatio / bestIndex["Notional"] * input_dict["Portfolio"]["Value"] / bestIndex["IndexFuturePrice"]
    output["OptimalHedgeRatio"] = round_num(optimalHedgeRatio, 3)
    output["NumFuturesContract"] = round_num(num)
    return output

# def round_num(number, n = None):
#     return round(number, n)

# def round_num(number, n = None):
#     if n:
#         return math.ceil(number * (10**n))/(10**n)
#     else: 
#         return math.ceil(number)

def round_num(number, n = None):
    if n:
        return round(round(number, n+1), n)
    else: 
        return round(round(number, 1))