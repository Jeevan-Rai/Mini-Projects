import re
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
import os
from sqlalchemy import exists
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect

with open('config.json', 'r') as c:
    params = json.load(c)['params']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
db = SQLAlchemy(app)

class Complainer(db.Model):
    C_NO = db.Column(db.Integer, primary_key=True)
    C_NAME = db.Column(db.String(10), nullable=False)
    C_ADDRESS = db.Column(db.String(120), nullable=False)
    C_PHONE = db.Column(db.Integer, nullable=False)
    C_AGE = db.Column(db.Integer, nullable=False)
    GENDER = db.Column(db.String(10), nullable=False)
    PASSWORD = db.Column(db.String(8), nullable=False)

class Crime(db.Model):
    CRIME_ID = db.Column(db.Integer, primary_key=True)
    CR_DESC = db.Column(db.String(200), nullable=False)
    CR_PLACE = db.Column(db.String(120), nullable=False)
    CR_DATE = db.Column(db.Date, nullable=False)
    CR_TIME = db.Column(db.Time, nullable=False)
    C_NO = db.Column(db.Integer, ForeignKey(Complainer.C_NO),nullable=False)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Complainer.C_NAME).filter_by(
            C_NAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_usr"] = uname
            return redirect('/complains')
        else:
            return redirect('/signup')
    return render_template('login.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if(request.method == "POST"):
        try:
            name = request.form.get("name")
            age = request.form.get("age")            
            phno = request.form.get("phno")
            gender = request.form.get("gender")
            address = request.form.get("address")
            psw = request.form.get("psw")
            entry = Complainer(C_NAME=name, C_ADDRESS=address, C_PHONE=phno,
                             C_AGE=age, GENDER=gender, PASSWORD=psw)
            params['crnt_usr'] = name
            db.session.add(entry)
            db.session.commit()
            return redirect("/")
        except:
            redirect("/signup")
    return render_template('signup.html')

@app.route("/complains", methods=["GET","POST"])
def complains():
    if(request.method=="POST"):
        # try:
            desc = request.form.get('desc')
            date = request.form.get('date')
            time = request.form.get('time')
            place = request.form.get('place')
            cno=db.session.query(Complainer.C_NO).filter_by(C_NAME=params['crnt_usr']).first()
            entry = Crime(CR_DESC=desc,CR_DATE=date,CR_TIME=time,CR_PLACE=place,C_NO=cno[0])
            db.session.add(entry)
            db.session.commit()
            return redirect("/")
        # except:
            redirect("/signin")
    return render_template('complains.html')

app.run(debug=True)
