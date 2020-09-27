import logging
import json
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluate_maze():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    tests = data.get("tests")
    result = {case_id:solve_maze(case.get("maze"), case.get("start"), case.get("end")) for case_id, case in tests}
    result = {"answers": result}
    logging.info("My result :{}".format(result))
    return jsonify(result)


def solve_maze(maze, start, end):
    M = {(r, c) for r, l in enumerate(maze) for c in range(len(l)) if l[c] == 0}
    start = {tuple(reversed(start))}
    h = 0
    M.difference_update(start)
    end = tuple(reversed(end))
    while end not in start:
        new = {(r, c) for r, c in M if {(r, c+1), (r, c-1), (r+1, c), (r-1, c)}.intersection(start)}
        if not new:
            return -1
        M.difference_update(new)
        start.update(new)
        h += 1
    return h