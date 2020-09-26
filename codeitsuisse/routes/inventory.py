import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluate_inventory():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests")
    result = {case_id:clean_floor(case.get("floor")) for case_id, case in tests.items()}
    result = {"answers": result}
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def clean_floor(floors):
    pos = 0
    max_pos = len(floors) - 1
    total = sum(floors)
    steps = 0

    while total>0:
        if (pos == 0) or (floors[pos-1]==0 and pos<max_pos):
            pos += 1
        else:
            pos -= 1
        steps += 1

        if (floors[pos] > 0):
            floors[pos] -= 1
            total -= 1
        else:
            floors[pos] = 1
            total += 1
    return steps

# test comment
    



