import logging
import numpy as np
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputs = data
    outputs = []
    for inp in inputs:
        item_name = inp["searchItemName"]
        output = {
            "searchItemName":item_name,
            "searchResult":[]}
        distances = [lev_mat(item_name, i) for i in inp["items"]]
        distances.sort()
        output["searchResult"] = [i[1] for i in distances[:10]]
        outputs.append(output)
    logging.info("My result :{}".format(output))
    return jsonify(outputs)

import numpy as np

def lev_mat(item, search):
    item = item.upper()
    search = search.upper()
    mat = np.zeros((len(item)+1, len(search)+1))
    mat[0] = [i for i in range(len(mat[0]))]
    mat[:, 0] = [i for i in range(len(mat[0:, ]))]
    for i in range(1, len(mat)):
        for j in range(1, len(mat[i])):
            add = mat[i-1][j] + 1
            rem = mat[i][j-1] + 1
            diag = mat[i-1][j-1] + int(item[i-1]!=search[j-1])
            mat[i][j] = min(add, rem, diag)
    moves = ""
    i, j = 1, 1
    while (i, j) != (len(item)+1, len(search)+1):

        if (i+1, j+1) != (len(item), len(search)) and (i, j) != (len(item), len(search)):
            add = mat[i][j+1]
            rem = mat[i+1][j]
            choice = mat[i+1][j+1]
            if j+1 == len(search):
                choice = rem
                moves += '-' + item[i-1]
                i += 1
            elif i+1 == len(item):
                choice = add
                moves += '+' + search[j-1]
                j += 1
            else:
                min_path = min(choice, add, rem)
                if min_path == choice:
                    moves += search[j-1]
                    i += 1
                    j += 1
                elif add<=rem:
                    choice = add
                    moves += '+' + search[j-1]
                    j += 1
                else:
                    choice = rem
                    moves += '-' + item[i-1]
                    i += 1
        else:
            moves += search[j-1]
            i += 1
            j += 1
    return mat[i-1][j-1], moves






