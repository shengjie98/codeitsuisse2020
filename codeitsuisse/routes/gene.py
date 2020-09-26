import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateGene():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    id_ = data.get("runId");
    list_ = data.get("list");

    result = {
        "runId": id_,
        "list": [
            {
                "id": x["id"],
                "geneSequence": rearrange(x["geneSequence"])
            } for x in list_
        ]
    }
    logging.info("My result :{}".format(result))
    return json.dumps(result);

def rearrange(gene):
    numOfGenomes = {x: gene.count(x) for x in {*[c for c in gene]}}
    numACGT = min(numOfGenomes.values())
    numCC = (numOfGenomes["C"]-numACGT)//2
    if (numOfGenomes["C"]-numACGT)%2 == 1 and numACGT > 0:
        numACGT -= 1
        numCC += 1
    remainder = {x: numOfGenomes[x]-numACGT for x in numOfGenomes.keys()}
    remainder["C"] -= numCC * 2
    result = []
    # 3 scanarios
    for i in range(numCC):
        if remainder["A"] >= 2:
            result.append("AA")
            remainder["A"] -= 2
        result.append("CC")
    for i in range(numACGT):
        if remainder["A"] >= 1:
            result.append("A")
            remainder["A"] -= 1
        result.append("ACGT")
    for x in ["C", "G", "T"]:
        for i in range(remainder[x]):
            if remainder["A"] >= 2:
                result.append("AA")
                remainder["A"] -= 2
            result.append(x)
    result.append("A" * remainder["A"])
    result = "".join(result)
    return result


