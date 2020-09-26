from flask import Flask
app = Flask(__name__)

import codeitsuisse.routes.saladspree
import codeitsuisse.routes.revisit
import codeitsuisse.routes.encrypt
import codeitsuisse.routes.square