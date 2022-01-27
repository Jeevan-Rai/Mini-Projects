from http.client import FORBIDDEN
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask import request
import json
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/automotive_showroom'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class Manufacturer(db.Model):
    M_ID = db.Column(db.Integer, primary_key=True)
    M_NAME = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    PHONE_NO = db.Column(db.Integer, nullable=False)


class Car_model(db.Model):
    CAR_ID = db.Column(db.Integer, primary_key=True)
    COST = db.Column(db.Integer, nullable=False)
    FUEL_TYPE = db.Column(db.String, nullable=False)
    YEAR_OF_LAUNCH = db.Column(db.Integer, nullable=False)
    M_ID = db.Column(db.Integer, ForeignKey(Manufacturer.M_ID), nullable=False)


class Showroom_branch(db.Model):
    B_ID = db.Column(db.Integer, primary_key=True)
    LOCATION = db.Column(db.String, nullable=False)


class Employee(db.Model):
    EMP_ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String, nullable=False)
    PHONE_NUMBER = db.Column(db.Integer, nullable=False)
    B_ID = db.Column(db.Integer, ForeignKey(Showroom_branch.B_ID))

class Customer(db.Model):
    CUST_ID = db.Column(db.Integer, primary_key=True)
    CUST_NAME = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    PHONE_NO = db.Column(db.Integer, nullable=False)
    # SER_ID = db.Column(db.Integer, ForeignKey(Support_System.SER_ID))
    CAR_ID = db.Column(db.Integer, ForeignKey(Car_model.CAR_ID))
    USERNAME = db.Column(db.String, nullable=False)
    PASSWORD = db.Column(db.String, nullable=False)

class Support_System(db.Model):
    SER_ID = db.Column(db.Integer, primary_key=True)
    MACHINARY_TOOLS = db.Column(db.String, nullable=False)
    CUST_ID = db.Column(db.Integer, ForeignKey(
        Customer.CUST_ID), nullable=False)
    EMP_ID = db.Column(db.Integer, ForeignKey(Employee.EMP_ID), nullable=False)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/u_signup",methods=["GET","POST"])
def signup():
    if(request.method == "POST"):
        # try:
            fname = request.form.get("Fname")
            lname = request.form.get("Lname")
            email = request.form.get("email")
            phno = request.form.get("phno")
            gender = request.form.get("gender")
            address = request.form.get("address")
            uname = request.form.get("username")
            psw = request.form.get("psw")
            entry = Customer(CUST_NAME=fname, address=address, PHONE_NO=phno,
                             USERNAME=uname, PASSWORD=psw)
            db.session.add(entry)
            # data = db.session.query(Customer.CUST_ID).filter_by(
            #     USERNAME=uname).first()
            # db.session.flush()
            # entry1 = Cart(CUST_ID=data[0])
            # db.session.add(entry1)
            db.session.commit()
            return redirect("/")
        # except:
            redirect("/u_signup")
    return render_template("u_signup.html")
@app.route("/u_login",methods=["GET","POST"])
def login():
    if(request.method == "POST"):
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        exists = db.session.query(Customer.USERNAME).filter_by(
            USERNAME=uname, PASSWORD=psw).first() is not None
        if(exists):
            # params["crnt_usr"] = uname
            session['cust_login'] = True
            return redirect('/')
        else:
            return redirect('/u_signup')
    return render_template('u_login.html')


app.run(debug=True)