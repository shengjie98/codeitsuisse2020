import logging
import socket
from codeitsuisse import app
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def default_route():
    return "Python Template"


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
<<<<<<< HEAD
    app.run(port=7000)
=======
    app.run(port=8000)
>>>>>>> 50fd33b70b50c06df3bf71ed4ec23f1ccae88e66
