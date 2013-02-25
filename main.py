# do not change the following basic imports and configurations  if you still want to use box.py
import settings

from flask import Flask
app = Flask(__name__)
app.config.from_object('settings')

# flask imports
from flask import g
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask import render_template
from flask import abort
from flask import flash
from flask import get_flashed_messages
from flask import json

# data model imports
from models import User, Balance, Transactions

# you can freely change the lines below

# package imports
import logging
import hashlib
from datetime import datetime
from helpers import generate_key

# google api and library imports
from google.appengine.api import taskqueue, images, mail, urlfetch
from google.appengine.ext import ndb
from google.appengine.api.labs import taskqueue

# global variables

# home root controller
@app.route('/')
def index():
    #define your controller here
    if 'user' in session:
    	return redirect(url_for('home_control'))
    else:
    	return render_template('welcome.html')

########### user data model controllers area ###########

def get_single_user(user_id):
	user = None
	single_user = User.query(User.user_id == user_id).get()
	if single_user:
		user = single_user.dto()
	result = user
	return result

@app.route('/profile')
def view_profile():
	#this is the controller to get single entry view
	if 'user' in session:
		user_id = session['user']['user_id']
		user = get_single_user(user_id)
		return render_template('user_view.html', user = user)
	else:
		return redirect(url_for('login_control'))

@app.route('/register/process')
def register_process_controller():
	email = request.values.get('email')
	firstname = request.values.get('firstname')
	lastname = request.values.get('lastname')
	password = request.values.get('password')
	hasher = hashlib.sha256()
	hasher.update(password)
	password = hasher.hexdigest()
	user_new_id = generate_key()

	new_user = User(
									user_id = user_new_id,
									email = email,
									firstname = firstname,
									lastname = lastname,
									password = password,
									join_date = datetime.now()
								)

	new_user.put()
	session['user'] = new_user.dto()
	return redirect(url_for('home_control'))

@app.route('/user/edit/<id>')
def user_edit_controller(id):
	#this is the controller to edit model entries
	user_item = User.query(User.user_id == id).get()
	return render_template('user_edit.html', user_item = user_item, title = "Edit Entries")

@app.route('/user/update/<id>',methods=['POST','GET'])
def user_update_data_controller(id):
	# this is the user data update handler
	firstname = request.values.get('firstname')
	lastname = request.values.get('lastname')
	user_item = User.query(User.user_id == id).get()
	user_item.firstname = firstname
	user_item.lastname = lastname

	User.put(user_item)

	return redirect(url_for('view_profile'))

########### balance data model controllers area ###########

@app.route('/balance/')
def balance_view_controller():
	#this is the controller to view all data in the model
	if "user" in session:
		balance_list = Balance.query(ndb.OR(Balance.payee == session['user']['email'],Balance.payer == session['user']['email'])).fetch(1000)
		
		if balance_list:
			balance_entries = [balance.dto() for balance in balance_list]
		else:
			balance_entries = None

		return render_template('balance.html',balance_entries = balance_entries, title = "Balance List")
	else:
		return redirect(url_for('login_control'))

########### transactions data model controllers area ###########

@app.route('/transactions/')
def transactions_view_controller():
	#this is the controller to view all data in the model
	if "user" in session:
		transactions_list = Transactions.query(ndb.OR(Transactions.payer==session['user']['email'],Transactions.payee==session['user']['email'])).fetch(10000)

		if transactions_list:
			transactions_entries = [transactions.dto() for transactions in transactions_list]
		else:
			transactions_entries = None

		return render_template('transactions.html',transactions_entries = transactions_entries, title = "Transactions List")
	else:
		return redirect(url_for('login_control'))

@app.route('/transactions/add/')
def transactions_add_controller():
	#this is the controller to add new model entries
	return render_template('transactions_add.html', title = "Add New Entry")

@app.route('/transactions/create/',methods=['POST','GET'])
def transactions_create_data_controller():
	# this is the transactions data create handler
	if 'user' in session:
		amount = float(request.values.get('amount'))
		payee = request.values.get('payee')
		payer = session['user']['email']
		description = request.values.get('description')

		transactions_new_id = generate_key()

		new_transactions = Transactions(
										transactions_id = transactions_new_id,
										amount = amount,
										payee = payee,
										payer = payer,
										description = description,
										transaction_time = datetime.now()
									)

		new_transactions.put()

		balance_check = Balance.query(Balance.payer == payer, Balance.payee == payee).get()
		if balance_check:
			balance_check.amount += amount
			Balance.put(balance_check)

		else:

			check_vice_versa = Balance.query(Balance.payee == payer, Balance.payer == payee).get()
			
			if check_vice_versa:
				
				if check_vice_versa.amount < amount:
					delta = amount - check_vice_versa.amount
					check_vice_versa.amount = 0
					Balance.put(check_vice_versa)
					amount = delta
				
				elif check_vice_versa.amount > amount:
					check_vice_versa.amount -= amount
					Balance.put(check_vice_versa)
					amount = 0
				
				else:
					check_vice_versa.amount = 0
					Balance.put(check_vice_versa)
					amount = 0
				
				if amount > 0:
					balance_new_id = generate_key()
				
					new_balance = Balance(
										balance_id = balance_new_id,
										payee = payee,
										payer = payer,
										amount = amount
									)
					new_balance.put()
			else:
				balance_new_id = generate_key()
				new_balance = Balance(
										balance_id = balance_new_id,
										payee = payee,
										payer = payer,
										amount = amount
									)
				new_balance.put()
		
		return redirect(url_for('home_control'))
	
	else:
		return redirect(url_for('login_control'))


@app.route('/login', methods=['GET','POST']) #Link
def login_control():
	# add your controller here
	if request.method == 'POST':
		email = request.values.get('email')
		password = request.values.get('password')
		hasher = hashlib.sha256()
		hasher.update(password)
		password = hasher.hexdigest()
		check_user = User.query(User.email == email, User.password == password).get()
		if check_user:
			session['user'] = check_user.dto()
			return redirect(url_for('home_control'))
	else:
		return render_template('login.html')

@app.route('/logout')
def logout_control():
	session.pop('user',None)
	return redirect(url_for('index'))

@app.route('/home/') #Link
def home_control():
	# add your controller here
	if 'user' in session:
		user = session['user']
		owe_you = Balance.query(Balance.payee == user['email'],Balance.amount != 0).fetch(10000)
		you_owe = Balance.query(Balance.payer == user['email'],Balance.amount != 0).fetch(10000)
		payer = []
		payee = []
		if owe_you:
			payee = [item.dto() for item in owe_you]
		else:
			payee = None
		if you_owe:
			payer = [item.dto() for item in you_owe]
		else:
			payer = None
		return render_template('home.html',user=user,payer=payer,payee=payee)
	else:
		return render_template('login.html')

@app.route('/register/') #Link
def register_control():
	# add your controller here
	return render_template('register.html')

@app.route('/pay/to/<email>',methods=['POST','GET'])
def pay_to_friend(email):
	if request.method == 'POST':
		payer = session['user']['email']
		amount = float(request.values.get('amount'))
		description = request.values.get('description')
		transactions_new_id = generate_key()

		new_transactions = Transactions(
										transactions_id = transactions_new_id,
										amount = amount,
										payee = email,
										payer = payer,
										description = description,
										transaction_time = datetime.now()
									)

		new_transactions.put()

		balance_to_pay = Balance.query(Balance.payee == email, Balance.payer == payer).get()
		if balance_to_pay:
			if amount > balance_to_pay.amount:
				delta = amount - balance_to_pay.amount
				balance_to_pay.amount = 0
				Balance.put(balance_to_pay)
				amount = delta
			elif amount < balance_to_pay.amount:
				balance_to_pay.amount -= amount
				Balance.put(balance_to_pay)
				amount = 0
			else:
				balance_to_pay.amount = 0
				Balance.put(balance_to_pay)
				amount = 0
			if amount > 0:
				balance_new_id = generate_key()
				new_balance = Balance(
								balance_id = balance_new_id,
								payee = payer,
								payer = email,
								amount = float(amount)
							)
				new_balance.put()

				transactions_new_id = generate_key()
				new_transactions = Transactions(
										transactions_id = transactions_new_id,
										amount = amount,
										payee = payer,
										payer = email,
										description = "Payment Excess Treated as deposit",
										transaction_time = datetime.now()
									)
				new_transactions.put()
		else:
			check_vice_versa = Balance.query(Balance.payee == payer, Balance.payer == email).get()
			if check_vice_versa:
				check_vice_versa.amount += amount
				Balance.put(check_vice_versa)
			else:
				balance_new_id = generate_key()
				new_balance = Balance(
								balance_id = balance_new_id,
								payee = payer,
								payer = email,
								amount = float(amount)
							)
				new_balance.put()	
		return redirect(url_for('home_control'))
	else:
		payer = session['user']['email']
		balance_detail = Balance.query(Balance.payer == payer, Balance.payee == email).get()
		if not balance_detail:
			balance_new_id = generate_key()
			balance_detail = Balance(
								balance_id = balance_new_id,
								payee = email,
								payer = payer,
								amount = 0
							)
		return render_template('pay_friend.html',balance=balance_detail.dto())