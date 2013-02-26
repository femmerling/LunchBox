# do not change the following basic imports and configurations  if you still want to use box.py
import settings

from flask import Flask
app = Flask(__name__)
app.config.from_object('settings')

# flask imports
#from flask import g
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask import render_template
#from flask import abort
#from flask import flash
#from flask import get_flashed_messages
from flask import json

# data model imports
from models import User, Balance, Transactions

# you can freely change the lines below

# package imports
import logging
import hashlib
from datetime import datetime
from helpers import generate_key,thousand_separator

# google api and library imports
from google.appengine.api import mail
from google.appengine.ext import ndb

# global variables
def mail_on_pay(payer,payee,name,amount,detail):
	mail_recipient = payee
	mail_subject = "Your friend "+name+ " has recorded a new transaction on you!"
	mail_body_admin = """
	Dear """+payee+""",

	Your friend """+name+""" has recorded a new transaction on you!

	The detail is as follows:

	Transaction amount: """+str(thousand_separator(int(amount)))+"""
	Transaction purpose: """+ detail +"""
	
	Login to LunchBox to see your detail

	thank you

	LunchBox Team
	http://ice-lunchbox.appspot.com
	

	automatic LunchBox notification system
	"""
	message_admin = mail.EmailMessage(
	                sender  = 'LunchBox Administrator <emmerling@icehousecorp.com>',
	                subject = mail_subject
	              )
	message_admin.to = mail_recipient
	message_admin.body = mail_body_admin
	message_admin.send()

	self_recipient = payer
	self_subject = "Reminder on deposit"
	self_body = """
	Dear """+payer+""",

	this is to remind you of a your new transaction to """+ payee+"""

	The detail is as follows:

	Transaction amount: """+str(thousand_separator(int(amount)))+"""
	Transaction purpose: """+ detail +"""
	
	Login to LunchBox to see your detail

	thank you

	LunchBox Team
	http://ice-lunchbox.appspot.com
	

	automatic LunchBox notification system
	"""
	self_send = mail.EmailMessage(
	                sender  = 'LunchBox Administrator <emmerling@icehousecorp.com>',
	                subject = self_subject
	              )
	self_send.to = self_recipient
	self_send.body = self_body
	self_send.send()

def mail_on_void(payer,payee,name,amount,detail):
	mail_recipient = payee
	mail_subject = "Your friend "+name+ " has voided a transaction!"
	mail_body_admin = """
	Dear """+payee+""",

	Your friend """+name+""" has voided one of your transaction.

	The detail is as follows:

	Transaction amount: """+str(thousand_separator(int(amount)))+"""
	Transaction purpose: """+ detail +"""
	
	Login to LunchBox to see your detail

	thank you

	LunchBox Team
	http://ice-lunchbox.appspot.com
	

	automatic LunchBox notification system
	"""
	message_admin = mail.EmailMessage(
	                sender  = 'LunchBox Administrator <emmerling@icehousecorp.com>',
	                subject = mail_subject
	              )
	message_admin.to = mail_recipient
	message_admin.body = mail_body_admin
	message_admin.send()

	self_recipient = payer
	self_subject = "Reminder on deposit"
	self_body = """
	Dear """+payer+""",

	this is to remind you that you have voided """+ payee+"""'s transaction'

	The detail is as follows:

	Transaction amount: """+str(thousand_separator(int(amount)))+"""
	Transaction purpose: """+ detail +"""
	
	Login to LunchBox to see your detail

	thank you

	LunchBox Team
	http://ice-lunchbox.appspot.com
	

	automatic LunchBox notification system
	"""
	self_send = mail.EmailMessage(
	                sender  = 'LunchBox Administrator <emmerling@icehousecorp.com>',
	                subject = self_subject
	              )
	self_send.to = self_recipient
	self_send.body = self_body
	self_send.send()

def mail_on_register(email,first_name,last_name):
	mail_recipient = email
	mail_subject = "Welcome to ICE-Pin"
	mail_body_admin = """
	Dear """+first_name+""" """+last_name+""",

	Welcome to ICE-Pin!

	We hope that you enjoy using our app.

	Your email """+email+""" is used as your username in this app.
	
	Login to LunchBox to see your detail.

	Enjoy your time with LunchBox!

	thank you

	LunchBox Team
	http://ice-lunchbox.appspot.com
	

	automatic LunchBox notification system
	"""
	message_admin = mail.EmailMessage(
	                sender  = 'ICE-Pin Administrator <emmerling@icehousecorp.com>',
	                subject = mail_subject
	              )
	message_admin.to = mail_recipient
	message_admin.body = mail_body_admin
	message_admin.send()

	admin_notify_to = "emmerling@icehousecorp.com"
	admin_body = "new user "+email+" have registered"
	
	send_admin = mail.EmailMessage(
					sender  = 'ICE-Pin Administrator <emmerling@icehousecorp.com>',
	                subject = "New Member Registered"
				)
	send_admin.to = admin_notify_to
	send_admin.body = admin_body
	send_admin.send()

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

@app.route('/register/process',methods=['GET','POST'])
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
	mail_on_register(email,firstname,lastname)
	return redirect(url_for('home_control'))

@app.route('/mobile/register',methods=['GET','POST'])
def mobile_register_process():
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
	mail_on_register(email,firstname,lastname)
	return str(new_user.dto())

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
		friends = []
		if transactions_list:
			transactions_entries = [transactions.dto() for transactions in transactions_list]
			for item in transactions_entries:
				if item['payer'] != session['user']['email']:
					if item['payer'] not in friends:
						friends.append(item['payer'])
				if item['payee'] != session['user']['email']:
					if item['payee'] not in friends:
						friends.append(item['payee'])
		else:
			transactions_entries = None
		if len(friends) == 0:
			friends = None

		return render_template('transactions.html',transactions_entries = transactions_entries, user_self=session['user']['email'],friends=friends, title = "Transactions List")
	else:
		return redirect(url_for('login_control'))

@app.route('/void/<trans_id>')
def void_trans(trans_id):
	void_trans = Transactions.query(Transactions.transactions_id == trans_id).get()
	payee = void_trans.payee
	payer = void_trans.payer
	amount = void_trans.amount
	description = void_trans.description
	update_balance = Balance.query(Balance.payee == payee, Balance.payer == payer).get()
	result = update_balance.amount - amount
	logging.error('### result')
	logging.error(result)
	if result >= 0:
		update_balance.amount -= amount
		Balance.put(update_balance)
	else:
		update_balance.amount = 0
		Balance.put(update_balance)
		result_balance = abs(result)
		balance_new_id = generate_key()
		check_vice_versa = Balance.query(Balance.payee == payer, Balance.payer == payee).get()
		if check_vice_versa:
			check_vice_versa.amount += result_balance
			Balance.put(check_vice_versa)
		else:
			new_balance = Balance(
								balance_id = balance_new_id,
								payee = payer,
								payer = payee,
								amount = result_balance
							)
			new_balance.put()
	void_trans.key.delete()
	name=session['user']['firstname']+" " +session['user']['lastname']
	mail_on_void(payer,payee,name,amount,description)
	return redirect(url_for('transactions_view_controller'))

@app.route('/transactions/add/')
def transactions_add_controller():
	#this is the controller to add new model entries
	return render_template('transactions_add.html', title = "Add New Transaction")

@app.route('/transactions/create/',methods=['POST','GET'])
def transactions_create_data_controller():
	# this is the transactions data create handler
	if 'user' in session:
		amount = float(request.values.get('amount'))
		payee = request.values.get('payee')
		payer = session['user']['email']
		description = request.values.get('description')
		if description == "":
			description = " "

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
		name=session['user']['firstname']+" " +session['user']['lastname']
		mail_on_pay(payer,payee,name,amount,description)

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
		
		return redirect(url_for('home_control',msg="Deposit done"))
	
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
			return render_template('login.html',msg="User does not exist")
	else:
		return render_template('login.html')

@app.route('/mobile/login', methods=['GET','POST']) #Link
def mobile_login_control():
	email = request.values.get('email')
	password = request.values.get('password')
	hasher = hashlib.sha256()
	hasher.update(password)
	password = hasher.hexdigest()
	check_user = User.query(User.email == email, User.password == password).get()
	if check_user:
		return str(check_user.dto())
	else:
		return "failed"

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

@app.route('/pay/friend', methods=['GET','POST'])
def pay_friend_control():
	if 'user' in session:
		if request.method == 'POST':
			payer = session['user']['email']
			payee = request.values.get('email')
			amount = float(request.values.get('amount'))
			description = request.values.get('description')
			if description == "":
				description = " "
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
			
			name=session['user']['firstname']+" " +session['user']['lastname']
			mail_on_pay(payer,payee,name,amount,description)

			balance_to_pay = Balance.query(Balance.payee == payee, Balance.payer == payer).get()
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
									payer = payee,
									amount = float(amount)
								)
					new_balance.put()

					transactions_new_id = generate_key()
					new_transactions = Transactions(
											transactions_id = transactions_new_id,
											amount = amount,
											payee = payer,
											payer = payee,
											description = "Payment Excess Treated as deposit",
											transaction_time = datetime.now()
										)
					new_transactions.put()
			else:
				check_vice_versa = Balance.query(Balance.payee == payer, Balance.payer == payee).get()
				if check_vice_versa:
					check_vice_versa.amount += amount
					Balance.put(check_vice_versa)
				else:
					balance_new_id = generate_key()
					new_balance = Balance(
									balance_id = balance_new_id,
									payee = payer,
									payer = payee,
									amount = float(amount)
								)
					new_balance.put()	
			return redirect(url_for('home_control',msg="Payment Done"))
		else:
			return render_template('pay_a_friend.html')
	else:
		return redirect(url_for('login_control'))

@app.route('/pay/to/<email>',methods=['POST','GET'])
def pay_to_friend(email):
	if request.method == 'POST':
		payer = session['user']['email']
		amount = float(request.values.get('amount'))
		description = request.values.get('description')
		if description == "":
			description = " "
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

		name=session['user']['firstname']+" " +session['user']['lastname']
		mail_on_pay(payer,email,name,amount,description)

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
		return redirect(url_for('home_control',msg="Payment Done!"))
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