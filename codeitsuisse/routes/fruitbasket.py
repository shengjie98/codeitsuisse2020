import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_data();
    logging.info("data sent for evaluation {}".format(data))
    # print(type(data))
    # print(data)
    # data = data.decode()
    # print(type(data))
    # print(data)

    
    # splitString = data.split(",")
    # noBanana = splitString[0]
    # noMelon = splitString[1]
    # noApple = splitString[2]
    # estimate = str(noApple*10+noBanana*10+noMelon*10)
    # result = estimate
    result = "1150"
    logging.info("My result :{}".format(result))
    return json.dumps(result);


# def getFruits(data):
#     fruitDict ={} #Fruits will be stored in a dictionary where the key is the fruit, and the value is the weight of it
#     fruitList = data.split(",")
#     firstFruit = fruitList[0]
#     print(firstFruit[])
    # secondFruit = fruitList[1]
    # thirdFruit = fruitList[2]

