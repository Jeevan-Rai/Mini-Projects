from http.client import FORBIDDEN
from django.shortcuts import render
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/courier'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class Customer(db.Model):
    CUST_ID = db.Column(db.Integer, primary_key=True)
    CUST_NAME = db.Column(db.String, nullable=False)
    E_MAIL = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    PHONE_NO = db.Column(db.Integer, nullable=False)
    GENDER = db.Column(db.String, nullable=False)
    USERNAME = db.Column(db.String, nullable=False)
    PASSWORD = db.Column(db.String, nullable=False)

class Couriers(db.Model):
    CR_ID = db.Column(db.Integer, primary_key=True)
    DESC = db.Column(db.String, nullable=False)
    TYPE = db.Column(db.String, nullable=False)
    DEL_ADD = db.Column(db.String, nullable=False)
    WEIGHT = db.Column(db.Integer, nullable=False)
    COST = db.Column(db.Integer, nullable=False)

@app.route("/")
def home():
    return render_template("c_index.html")

@app.route("/c_add",methods=["GET" , "POST"])
def add():
    if(request.method == "POST"):
        category = request.form.get("category")
        desc = request.form.get("desc")
        weight = request.form.get("weight")
        address = request.form.get("address")
        entry = Couriers(TYPE=category, DESC=desc, DEL_ADD=address,WEIGHT=weight,COST=weight*29)
        db.session.add(entry)
        db.session.commit
        redirect("/")
    return render_template("c_add.html")



app.run(debug=True)