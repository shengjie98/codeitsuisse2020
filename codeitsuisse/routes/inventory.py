import logging
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
        distances = [get_changes(item_name, i) for i in inp["items"]]
        distances.sort(reverse=True)
        output["searchResult"] = distances[:10]
        outputs.append(output)
    logging.info("My result :{}".format(output))
    return jsonify(output)

def find_index(seq, word):
    for i in range(len(word)):
        if word[i:i+len(seq)] == seq:
            return i
    return -1

def next_common(word1, word2):
    dict1 = {}
    dict2 = {}
    nearest_common = -1

    for i in range(len(word1)):
        if dict1.get(word1[i]) is None:
            dict1[word1[i]] = i
    for i in range(len(word2)):
        if dict2.get(word2[i]) is None:
            dict2[word2[i]] = i
    
    for i in word1:
        dist = dict2.get(i)
        if (dist != None):
            if (nearest_common == -1) or (dist<nearest_common):
                nearest_common = dist
    return nearest_common


def get_changes(item, search):
    num_moves = 0
    out_str = ""
    while (item != "") and (search != ""):
        if (item[0] == search[0]):
            out_str += item[0]
            item = item[1:]
            search = search[1:]
        
        else:
            num_moves += 1
            # find the position of the next letter in the search string
            pos = find_index(item[0], search)
            next_pos = next_common(item, search)

            # case 1 addition
            if 0<pos<=next_pos:
                out_str += "+" + search[0]
                search = search[1:]
            # case 2 substitution
            elif (pos<0 and next_pos>=0) or (pos>0 and pos>next_pos):
                out_str += search[0]
                item = item[1:]
                search = search[1:]
            # case 3 removal
            else:
                out_str += "-" + item[0]
                item = item[1:]
    
    if (item != ""):
        out_str += "-" + "-".join(item)
    elif (search != ""):
        out_str += "+" + "+".join(search)
    
    return [num_moves, out_str]




