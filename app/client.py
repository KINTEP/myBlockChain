from flask import Flask, render_template, request, redirect, jsonify
import requests
from keys import PrivateKey, N
from helper import hash256
import random
from transactions import Transaction_In, Transaction_Out, Transaction
import json
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
import os
from datetime import datetime
from flask_login import UserMixin

app = Flask(__name__)

NODE = "http://127.0.0.1:8000"

basedir = os.path.abspath(os.path.dirname(__file__))


login_manager = LoginManager(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "skjskkhsajhkashshk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'myBlockChain.db')

login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime(), default = datetime.utcnow())
    keys = db.relationship('Keys', backref = 'owner', lazy = 'dynamic')

class Keys(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(100))
    private_key = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(), default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

all_posts = []

def fetch_post():
	response = requests.get(f"{NODE}/chain")
	data = response.json()["chain"]
	data1 = []
	data3 = []

	for i in range(len(data)):
		if i >= 1:
			data1.append(data[i]['transactions']['output']['data'])

	for x in data1:
		for t in x:
			data3.append(t)

	global all_posts
	all_posts = data3[::-1]


@app.route("/", methods = ['GET','POST'])
def home():
	req1 = request.host_url
	print(req1)
	req2 = requests.get(f"{req1}/get_private_key").json()
	#print(req2)
	fetch_post()
	global all_posts
	if request.method == "POST":
		title = request.form.get("title")
		content = request.form.get("content")
		private_key = req2["key"] #Transfer of private key doesnt look safe to me.
		phex = req2["phex"]
		address = req2["address"]
		if title and content:
			data = {
				"title": title,
				"content": content,
				}
			data_from = Transaction_In(prev_tx = "0", prev_idx = 0)
			data_to = Transaction_Out(amount = 0, data = [data], pubkey = address)
			trans = Transaction(input_ = data_from, output = data_to)
			z = int.from_bytes(hash256(trans.id().encode()), 'big')
			signature = trans.sign(z = z, secret = int(phex))
			#trans_hash = trans.id()
			#signed_trans = sign(trans_hash, secret = private_key)
			data1 = {
				"tx_id": trans.id(),
				"input": trans.input_.__dict__,
				"output": trans.output.__dict__,
				"signature": signature.__dict__
			}
			#print(f"This is the signed trans: {signed_trans}")
			address = f"{NODE}/add_to_chain"
			response = requests.post(url = address, 
									json = data1,
									headers = {'Content-type': 'application/json'})
			if response.status_code == 200:
				return redirect("/")
	return render_template("index.html", all_posts = all_posts)

@app.route("/connect", methods = ["POST",'GET'])
def connect():
	req = request.host_url
	return req

@app.route("/register", methods = ["GET", "POST"])
def register():
	if request.method == "POST":
		name = request.form.get("name")
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
	return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
	return render_template("login.html")

@app.route("/address", methods = ["GET", "POST"])
def address():
    users = User.query.all()
    if request.method == "POST":
        req = str(request.form.get("address"))
        if len(req) >= 1:
            sec = req.encode()
            secret = little_endian_to_int(hash256(sec))
            private_key = PrivateKey(secret)
            address = private_key.point.address(testnet=True)
            p_address = private_key.wif()
            #user = User(name = req, address = address, private_key = p_address)
            #db.session.add(user)
            #db.session.commit()
            return redirect(url_for('address'))
        return("Please make entry")
    return render_template("get_address.html", users = users)

@app.route("/get_private_key")
def get_private_key():
	secret = random.randint(1,N)
	private_key = PrivateKey(secret = secret)
	address = private_key.point.address(testnet=True)
	p_address = private_key.wif()
	p_hex = private_key.secret
	return jsonify({"key":p_address, "phex": p_hex, "address": address})

if __name__ == '__main__':
	app.run(debug = True)