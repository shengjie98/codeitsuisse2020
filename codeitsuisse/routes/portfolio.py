
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
    x_min = input_dict[0]
    x_min_HR = x_min["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x_min["FuturePrcVol"]
    x_min_num = x_min_HR / x_min["Notional"] * input_dict["Portfolio"]["Value"] / x_min["IndexFuturePrice"]
    for x in input_dict[1:]:
        new_HR =  x["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x["FuturePrcVol"]
        if new_HR < x_min_HR:
            x_min = x
            x_min_HR = new_HR
            x_min_num = x_min_HR / x_min["Notional"] * input_dict["Portfolio"]["Value"] / x_min["IndexFuturePrice"]
            # change min
        elif new_HR == x_min_HR:
            # check vol
            if x["FuturePrcVol"] < x_min["FuturePrcVol"]:
                x_min = x
                x_min_num = x_min_HR / x_min["Notional"] * input_dict["Portfolio"]["Value"] / x_min["IndexFuturePrice"]
            elif x["FuturePrcVol"] == x_min["FuturePrcVol"]:
                #check num
                new_x_num = x_min_HR / x["Notional"] * input_dict["Portfolio"]["Value"] / x["IndexFuturePrice"]
                if new_x_num < x_min_num:
                    x_min = x
                    x_min_num = new_x_num
    output = {
        "HedgePositionName" : x_min["Name"], 
        "OptimalHedgeRatio" : x_min_HR, 
        "NumFuturesContract": x_min_num
    }
    return output

# def round_num(number, n = None):
#     return round(number, n)

def round_num(number, n = None):
    if n:
        return math.ceil(number * (10**n))/(10**n)
    else: 
        return math.ceil(number)

# def round_num(number, n = None):
#     if n:
#         return round(round(number, n+1), n)
#     else: 
#         return round(round(number, 1))