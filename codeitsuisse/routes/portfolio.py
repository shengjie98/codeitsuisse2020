
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
    x_min = input_dict["IndexFutures"][0]
    for x in input_dict["IndexFutures"][1:]:
        x_min = compare(x_min, x, input_dict)
    vol = x_min["FuturePrcVol"]
    HR = round_num(x_min["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x_min["FuturePrcVol"], 3)
    num = round_num(HR / x_min["Notional"] * input_dict["Portfolio"]["Value"] / x_min["IndexFuturePrice"])
    output = {
        "HedgePositionName" : x_min["Name"], 
        "OptimalHedgeRatio" : (HR), 
        "NumFuturesContract": (num)
    }
    return output
        

def compare(x1, x2, input_dict):
    vol1 = x1["FuturePrcVol"]
    HR1 = round_num(x1["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x1["FuturePrcVol"], 3)
    num1 = round_num(HR1 / x1["Notional"] * input_dict["Portfolio"]["Value"] / x1["IndexFuturePrice"])        
    vol2 = x2["FuturePrcVol"]
    HR2 = round_num(x2["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x2["FuturePrcVol"], 3)
    num2 = round_num(HR2 / x2["Notional"] * input_dict["Portfolio"]["Value"] / x2["IndexFuturePrice"])

    if vol1==vol2 and HR1==HR2:
        if num1 <= num2:
            return x1
        else:
            return x2
    if vol1<=vol2 and HR1<=HR2:
        return x1
    elif vol2<=vol1 and HR2<=HR1:
        return x2
    elif num1 <= num2:
        return x1
    else:
        return x2


# def round_num(number, n = None):
#     return round(number, n)

def round_num(number, n = None):
    if n:
        return math.ceil(number * (10**n))/(10**n)
    else: 
        return math.ceil(number)
