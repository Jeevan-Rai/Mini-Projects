import re
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
from sqlalchemy import exists
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect
import base64

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


@app.route("/")
def home():
    prdts = db.session.query(Products.P_NAME,Products.COUNT,Products.COST,Products.P_IMG,Products.P_DESC).all()
    return render_template('c_index.html',products=prdts)
