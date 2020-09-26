import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_data();
    logging.info("data sent for evaluation {}".format(data))
    splitString = data.split(",")
    noBanana = splitString[0]
    noMelon = splitString[1]
    noApple = splitString[2]
    estimate = str(noApple*10+noBanana*10+noMelon*10)
    result = estimate
    logging.info("My result :{}".format(result))
    return json.dumps(result);


