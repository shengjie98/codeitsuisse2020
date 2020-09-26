import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # tests = data.get("tests")
    result = {"answer": cluster(data)}
    logging.info("My result :{}".format(result))
    return jsonify(result)

def cluster(grid):
    ones = [{(r, c)} for r, l in enumerate(grid) for c in range(len(l)) if l[c] == '1']
    all_ones = {(r, c) for r, l in enumerate(grid) for c in range(len(l)) if l[c] == '1'}
    for i, one in enumerate(ones):
        zeros = {(r, c) for r, l in enumerate(grid) for c in range(len(l)) if l[c] == '0'}
        other_ones = all_ones - one 
        while zeros:
            new_infected = {(r, c) for r, c in zeros if {(r, c+1), (r, c-1), (r+1, c), (r-1, c), (r+1, c+1), (r+1, c-1), (r+1, c+1), (r-1, c-1)}.intersection(one)}
            one.update(new_infected)
            zeros.difference_update(new_infected)
            reinfected = {(r, c) for r, c in other_ones if {(r, c+1), (r, c-1), (r+1, c), (r-1, c), (r+1, c+1), (r+1, c-1), (r+1, c+1), (r-1, c-1)}.intersection(one)}
            one.update(reinfected)
            other_ones.difference_update(reinfected)
            # print(not reinfected)
            if not reinfected and not new_infected:
                break
        # print("done")
    num = 0
    total_ones = set()
    for one in ones:
        if one.isdisjoint(total_ones):
            num += 1
            total_ones.update(one)

    return num