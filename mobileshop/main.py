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

app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Customer.USERNAME).filter_by(
            USERNAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_usr"] = uname
            session['cust_login'] = True
            return redirect('/')
        else:
            return redirect('/signup')
    return render_template('login.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if(request.method == "POST"):
        try:
            fname = request.form.get("Fname")
            lname = request.form.get("Lname")
            email = request.form.get("email")
            phno = request.form.get("phno")
            gender = request.form.get("gender")
            address = request.form.get("address")
            uname = request.form.get("username")
            psw = request.form.get("psw")
            entry = Customer(F_NAME=fname, L_NAME=lname, ADDRESS=address, PH_NO=phno,
                             E_MAIL=email, GENDER=gender, USERNAME=uname, PASSWORD=psw)
            db.session.add(entry)
            data = db.session.query(Customer.CUST_ID).filter_by(
                USERNAME=uname).first()
            db.session.flush()
            entry1 = Cart(CUST_ID=data[0])
            db.session.add(entry1)
            db.session.commit()
            return redirect("/")
        except:
            print
            redirect("/signup")
    return render_template('signup.html')

app.run(debug=True)
