from flask import Flask, render_template, request, Response, send_file
import mysql.connector
import json, time, uuid, ldap
from markupsafe import escape
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
import requests as req

from helpop import helpop
from permissions import permissions
from restrictions import restrictions
from login import login
from frontend import frontend
from validation import validation

app = Flask(__name__)
app.register_blueprint(frontend)
app.register_blueprint(helpop)
app.register_blueprint(permissions)
app.register_blueprint(restrictions)
app.register_blueprint(validation)
app.register_blueprint(login)
CORS(app)

app.run(host="localhost", port="8080", debug=True)
