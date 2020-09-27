import logging
import json
from io import StringIO
import pandas as pd

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/pre-tick', methods=['POST'])
def evaluate_tick():
    data = request.get_data()
    data = str(data, "utf-8")
    logging.info("data sent for evaluation {}".format(data))
    result = get_tick(data)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def get_tick(csvStr):
    data = StringIO(csvStr)
    df = pd.read_csv(data)
    T = len(df) -1
    # df = pd.DataFrame([x.split(';') for x in csvStr.split('\n')])
    cT = df["Close"].expanding(1).mean()
    zT = df["Close"].expanding(1).std()
    ans = (cT + zT).get(T)
    logging.info("df: ".format(str(T)))
    return ans