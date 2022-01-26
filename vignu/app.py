from http.client import FORBIDDEN
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/insurance'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class Customer(db.Model):
    CUST_ID = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String, nullable=False)
    PASSWORD = db.Column(db.String, nullable=False)
    PHONE_NO = db.Column(db.Integer, nullable=False)

class Schemes(db.Model):
    S_ID = db.Column(db.Integer, primary_key=True)
    DESC = db.Column(db.String, nullable=False)

@app.route("/")
def home():
    sch = db.session.query(Schemes.DESC).all()
    return render_template("c_index.html", sch=sch)

@app.route("/c_signup")
def signup():
    if(request.method == "POST"):
        try:
            uname = request.form.get("username")
            psw = request.form.get("psw")
            entry = Customer(USERNAME=uname, PASSWORD=psw)
            db.session.add(entry)
            db.session.commit()
            return redirect("/c_signin")
        except:
            print
            redirect("/c_signup")
    return render_template("c_signup.html")


@app.route("/c_login")
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Customer.USERNAME).filter_by(
            USERNAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            params["crnt_usr"] = uname
            session['c_loggedin'] = True
            return redirect('/')
        else:
            return redirect('/signup')
    return render_template('c_login.html')
app.run(debug=True)