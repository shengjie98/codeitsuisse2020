import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/xerox', methods=['POST'])
def evaluateXerox():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    # inputValue = data.get("input");
    # result = inputValue * inputValue
    logging.info("My result :{}".format(result))
    return json.dumps({ "document-id": [ { "from": 1, "to": 100, "copier": "M1" }, { "from": 101, "to": 200, "copier": "M2" } ] });