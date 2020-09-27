import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/yin-yang', methods=['POST'])
def evaluate_yy():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    elements = data.get("elements")
    elements = list(elements)
    number_of_operations = data.get("number_of_operations")
    result = 12
    logging.info("My result :{}".format(result))
    return jsonify(result)

def getMaxExp(state, k):
    n = len(state)
    # for each n, find E(state-nL) and E(state-nR)
    #    find E(l) and E(R)
    # max E(l) and E(r)
    # return max

    # if k == 1
    if k == 1:
        # greedy choose Y
        total = 0
        for i in range(n):
            # i from 0 to n-1
            if state[i] == "Y":
                total += 1
            elif state[-i-1] == "Y":
                total += 1
        expectation = total/n
        return expectation

    total = 0
    for i in range(n): 
        x = state.pop(i)
        l = getMaxExp(state, k-1)
        if x == "Y":
            l+=1
        state.insert(i, x)

        x = state.pop(-i-1)
        r = getMaxExp(state, k-1)
        if x == "Y":
            r+=1
        state.insert(((-i-1)%(n-1)) + 1, x)
        total += max(l, r)
    expectation = total/n
    return expectation