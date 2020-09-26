import logging
import json
import numpy as np

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def evaluateGeometry():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    shapeCoordinates = data.get("shapeCoordinates");
    lineCoordinates = data.get("lineCoordinates");
    result = naive_intersection(shapeCoordinates, lineCoordinates)
    logging.info("My result :{}".format(result))
    return json.dumps(result);

def naive_intersection(shapeCoordinates, lineCoordinates):
    lineDirection = { "x" : lineCoordinates[0]["x"] - lineCoordinates[1]["x"], "y" : lineCoordinates[0]["y"] - lineCoordinates[1]["y"]}
    results = []
    for i in range(-len(shapeCoordinates), 0):
        # A = [[d1x, -d2x], [d1y, -d2y]] 
        # b = [p2x - p1x, p2y - p2x]
        # where l1 = p1 + t*d1 is the line segment on the polygon
        # and l2 = p2 + s*d2 is the line 
        A = np.array([
            [shapeCoordinates[i+1]["x"] - shapeCoordinates[i]["x"] , -lineDirection["x"]], 
            [shapeCoordinates[i+1]["y"] - shapeCoordinates[i]["y"] , -lineDirection["y"]]
        ])
        b = np.array([
            lineCoordinates[0]["x"] - shapeCoordinates[i]["x"],
            lineCoordinates[0]["y"] - shapeCoordinates[i]["y"]
        ])

        x = np.linalg.solve(A, b)
        s = x[1]
        intersection = {
            "x" : lineCoordinates[0]["x"] + s * lineDirection["x"], 
            "y" : lineCoordinates[0]["y"] + s * lineDirection["y"]
        }
        # if intersection falls within the endpoints of l1
        if inBetween(intersection, shapeCoordinates[i], shapeCoordinates[i+1]):
            results.append(intersection)
    results = [dict(t) for t in {tuple(d.items()) for d in results}]
    return results

def inBetween(intersection, endpoint1, endpoint2):
    if intersection["x"] < endpoint1["x"] and intersection["x"] < endpoint2["x"]: 
        return False
    if intersection["x"] > endpoint1["x"] and intersection["x"] > endpoint2["x"]: 
        return False
    if intersection["y"] < endpoint1["y"] and intersection["y"] < endpoint2["y"]: 
        return False
    if intersection["y"] > endpoint1["y"] and intersection["y"] > endpoint2["y"]: 
        return False
    return True


