
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
    # bestIndex = min(input_dict["IndexFutures"], key = lambda x: x["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / x["FuturePrcVol"])
    output = {"HedgePositionName": bestIndex["Name"]}
    optimalHedgeRatio = bestIndex["CoRelationCoefficient"] * input_dict["Portfolio"]["SpotPrcVol"] / bestIndex["FuturePrcVol"]
    num = optimalHedgeRatio / bestIndex["Notional"] * input_dict["Portfolio"]["Value"] / bestIndex["IndexFuturePrice"]
    output["OptimalHedgeRatio"] = math.ceil(optimalHedgeRatio * 1000)/1000
    output["NumFuturesContract"] = math.ceil(num)
    return output