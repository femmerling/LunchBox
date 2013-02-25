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
    return render_template('welcome.html')


########### user data model controllers area ###########

@app.route('/data/user/')
def data_user():
	# this is the controller for JSON data access
	user_list = User.query().fetch(10000)

	if user_list:
		json_result = json.dumps([user.dto() for user in user_list])
	else:
		json_result = None

	return json_result

@app.route('/user/')
def user_view_controller():
	#this is the controller to view all data in the model
	user_list = User.query().fetch(1000)

	if user_list:
		user_entries = [user.dto() for user in user_list]
	else:
		user_entries = None

	return render_template('user.html',user_entries = user_entries, title = "User List")

def get_single_user(user_id):
	user = None
	single_user = User.query(User.user_id == user_id).get()
	if single_user:
		user = single_user.dto()
	result = user
	return result

@app.route('/user/<user_id>.json')
def get_single_user_json(user_id):
	#this is the controller to get single entry in json format
	result = json.dumps(dict(user=get_single_user(user_id)))
	return result

@app.route('/user/<user_id>')
def view_single_user(user_id):
	#this is the controller to get single entry view
	user = get_single_user(user_id)
	return render_template(user_view.html, user = user)

@app.route('/user/add/')
def user_add_controller():
	#this is the controller to add new model entries
	return render_template('user_add.html', title = "Add New Entry")

@app.route('/user/create/',methods=['POST','GET'])
def user_create_data_controller():
	# this is the user data create handler
	email = request.values.get('email')
	firstname = request.values.get('firstname')
	lastname = request.values.get('lastname')
	join_date = request.values.get('join_date')
	user_new_id = generate_key()

	new_user = User(
									user_id = user_new_id,
									email = email,
									firstname = firstname,
									lastname = lastname,
									join_date = join_date
								)

	new_user.put()

	return 'data input successful <a href="/user/">back to Entries</a>'

@app.route('/user/edit/<id>')
def user_edit_controller(id):
	#this is the controller to edit model entries
	user_item = User.query(User.user_id == id).get()
	return render_template('user_edit.html', user_item = user_item, title = "Edit Entries")

@app.route('/user/update/<id>',methods=['POST','GET'])
def user_update_data_controller(id):
	# this is the user data update handler
	email = request.values.get('email')
	firstname = request.values.get('firstname')
	lastname = request.values.get('lastname')
	join_date = request.values.get('join_date')
	user_item = User.query(User.user_id == id).get()
	user_item.email = email
	user_item.firstname = firstname
	user_item.lastname = lastname
	user_item.join_date = join_date

	User.put(user_item)

	return 'data update successful <a href="/user/">back to Entries</a>'

@app.route('/user/delete/<id>')
def user_delete_controller(id):
	#this is the controller to delete model entries
	user_item = User.query(User.user_id == id).get()

	user_item.key.delete()

	return 'data deletion successful <a href="/user/">back to Entries</a>'



########### balance data model controllers area ###########

@app.route('/data/balance/')
def data_balance():
	# this is the controller for JSON data access
	balance_list = Balance.query().fetch(10000)

	if balance_list:
		json_result = json.dumps([balance.dto() for balance in balance_list])
	else:
		json_result = None

	return json_result

@app.route('/balance/')
def balance_view_controller():
	#this is the controller to view all data in the model
	balance_list = Balance.query().fetch(1000)

	if balance_list:
		balance_entries = [balance.dto() for balance in balance_list]
	else:
		balance_entries = None

	return render_template('balance.html',balance_entries = balance_entries, title = "Balance List")

def get_single_balance(balance_id):
	balance = None
	single_balance = Balance.query(Balance.balance_id == balance_id).get()
	if single_balance:
		balance = single_balance.dto()
	result = balance
	return result

@app.route('/balance/<balance_id>.json')
def get_single_balance_json(balance_id):
	#this is the controller to get single entry in json format
	result = json.dumps(dict(balance=get_single_balance(balance_id)))
	return result

@app.route('/balance/<balance_id>')
def view_single_balance(balance_id):
	#this is the controller to get single entry view
	balance = get_single_balance(balance_id)
	return render_template(balance_view.html, balance = balance)

@app.route('/balance/add/')
def balance_add_controller():
	#this is the controller to add new model entries
	return render_template('balance_add.html', title = "Add New Entry")

@app.route('/balance/create/',methods=['POST','GET'])
def balance_create_data_controller():
	# this is the balance data create handler
	payee = request.values.get('payee')
	payer = request.values.get('payer')
	amount = request.values.get('amount')
	balance_new_id = generate_key()

	new_balance = Balance(
									balance_id = balance_new_id,
									payee = payee,
									payer = payer,
									amount = amount
								)

	new_balance.put()

	return 'data input successful <a href="/balance/">back to Entries</a>'

@app.route('/balance/edit/<id>')
def balance_edit_controller(id):
	#this is the controller to edit model entries
	balance_item = Balance.query(Balance.balance_id == id).get()
	return render_template('balance_edit.html', balance_item = balance_item, title = "Edit Entries")

@app.route('/balance/update/<id>',methods=['POST','GET'])
def balance_update_data_controller(id):
	# this is the balance data update handler
	payee = request.values.get('payee')
	payer = request.values.get('payer')
	amount = request.values.get('amount')
	balance_item = Balance.query(Balance.balance_id == id).get()
	balance_item.payee = payee
	balance_item.payer = payer
	balance_item.amount = amount

	Balance.put(balance_item)

	return 'data update successful <a href="/balance/">back to Entries</a>'

@app.route('/balance/delete/<id>')
def balance_delete_controller(id):
	#this is the controller to delete model entries
	balance_item = Balance.query(Balance.balance_id == id).get()

	balance_item.key.delete()

	return 'data deletion successful <a href="/balance/">back to Entries</a>'



########### transactions data model controllers area ###########

@app.route('/data/transactions/')
def data_transactions():
	# this is the controller for JSON data access
	transactions_list = Transactions.query().fetch(10000)

	if transactions_list:
		json_result = json.dumps([transactions.dto() for transactions in transactions_list])
	else:
		json_result = None

	return json_result

@app.route('/transactions/')
def transactions_view_controller():
	#this is the controller to view all data in the model
	transactions_list = Transactions.query().fetch(1000)

	if transactions_list:
		transactions_entries = [transactions.dto() for transactions in transactions_list]
	else:
		transactions_entries = None

	return render_template('transactions.html',transactions_entries = transactions_entries, title = "Transactions List")

def get_single_transactions(transactions_id):
	transactions = None
	single_transactions = Transactions.query(Transactions.transactions_id == transactions_id).get()
	if single_transactions:
		transactions = single_transactions.dto()
	result = transactions
	return result

@app.route('/transactions/<transactions_id>.json')
def get_single_transactions_json(transactions_id):
	#this is the controller to get single entry in json format
	result = json.dumps(dict(transactions=get_single_transactions(transactions_id)))
	return result

@app.route('/transactions/<transactions_id>')
def view_single_transactions(transactions_id):
	#this is the controller to get single entry view
	transactions = get_single_transactions(transactions_id)
	return render_template(transactions_view.html, transactions = transactions)

@app.route('/transactions/add/')
def transactions_add_controller():
	#this is the controller to add new model entries
	return render_template('transactions_add.html', title = "Add New Entry")

@app.route('/transactions/create/',methods=['POST','GET'])
def transactions_create_data_controller():
	# this is the transactions data create handler
	amount = request.values.get('amount')
	payee = request.values.get('payee')
	payer = request.values.get('payer')
	description = request.values.get('description')
	transaction_time = request.values.get('transaction_time')
	transactions_new_id = generate_key()

	new_transactions = Transactions(
									transactions_id = transactions_new_id,
									amount = amount,
									payee = payee,
									payer = payer,
									description = description,
									transaction_time = transaction_time
								)

	new_transactions.put()

	return 'data input successful <a href="/transactions/">back to Entries</a>'

@app.route('/transactions/edit/<id>')
def transactions_edit_controller(id):
	#this is the controller to edit model entries
	transactions_item = Transactions.query(Transactions.transactions_id == id).get()
	return render_template('transactions_edit.html', transactions_item = transactions_item, title = "Edit Entries")

@app.route('/transactions/update/<id>',methods=['POST','GET'])
def transactions_update_data_controller(id):
	# this is the transactions data update handler
	amount = request.values.get('amount')
	payee = request.values.get('payee')
	payer = request.values.get('payer')
	description = request.values.get('description')
	transaction_time = request.values.get('transaction_time')
	transactions_item = Transactions.query(Transactions.transactions_id == id).get()
	transactions_item.amount = amount
	transactions_item.payee = payee
	transactions_item.payer = payer
	transactions_item.description = description
	transactions_item.transaction_time = transaction_time

	Transactions.put(transactions_item)

	return 'data update successful <a href="/transactions/">back to Entries</a>'

@app.route('/transactions/delete/<id>')
def transactions_delete_controller(id):
	#this is the controller to delete model entries
	transactions_item = Transactions.query(Transactions.transactions_id == id).get()

	transactions_item.key.delete()

	return 'data deletion successful <a href="/transactions/">back to Entries</a>'

