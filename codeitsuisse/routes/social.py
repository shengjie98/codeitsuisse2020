import math
import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluate_social():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests")
    result = {case_id:distancing(case.get("seats"), case.get("people"), case.get("spaces")) for case_id, case in tests.items()}
    result = {"answers": result}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def distancing(seats, people, spaces):
    n = seats - (spaces * people) + spaces
    r = people
    if n<0 or r<0 or n-r<0:
        return 0
    return math.factorial(n) / (math.factorial(r) * math.factorial(n-r))
