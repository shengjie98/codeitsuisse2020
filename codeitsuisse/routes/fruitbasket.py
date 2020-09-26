import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    noBanana = data.get("maBanana");
    noMelon = data.get("maWatermelon")
    noApple = data.get("maApple")
    result = noApple*10+noBanana*10+noMelon*10
    logging.info("My result :{}".format(result))
    return json.dumps(result);


