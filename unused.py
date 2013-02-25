####################################################################################################
######################################## UNUSED GENERATED FUNCTIONS ################################
####################################################################################################

## user functions

# @app.route('/data/user/')
# def data_user():
# 	# this is the controller for JSON data access
# 	user_list = User.query().fetch(10000)

# 	if user_list:
# 		json_result = json.dumps([user.dto() for user in user_list])
# 	else:
# 		json_result = None

# 	return json_result

# @app.route('/user/')
# def user_view_controller():
# 	#this is the controller to view all data in the model
# 	user_list = User.query().fetch(1000)

# 	if user_list:
# 		user_entries = [user.dto() for user in user_list]
# 	else:
# 		user_entries = None

# 	return render_template('user.html',user_entries = user_entries, title = "User List")

# @app.route('/user/<user_id>.json')
# def get_single_user_json(user_id):
# 	#this is the controller to get single entry in json format
# 	result = json.dumps(dict(user=get_single_user(user_id)))
# 	return result

# @app.route('/user/<user_id>')
# def view_single_user(user_id):
# 	#this is the controller to get single entry view
# 	user = get_single_user(user_id)
# 	return render_template(user_view.html, user = user)

# @app.route('/user/add/')
# def user_add_controller():
# 	#this is the controller to add new model entries
# 	return render_template('user_add.html', title = "Add New Entry")

# @app.route('/user/create/',methods=['POST','GET'])
# def user_create_data_controller():
# 	# this is the user data create handler
# 	email = request.values.get('email')
# 	firstname = request.values.get('firstname')
# 	lastname = request.values.get('lastname')
# 	password = request.values.get('password')
# 	hasher = hashlib.sha256()
# 	hasher.update(password)
# 	password = hasher.hexdigest()
# 	user_new_id = generate_key()

# 	new_user = User(
# 									user_id = user_new_id,
# 									email = email,
# 									firstname = firstname,
# 									lastname = lastname,
# 									password = password,
# 									join_date = datetime.now()
# 								)

# 	new_user.put()

# 	return 'data input successful <a href="/user/">back to Entries</a>'

# @app.route('/user/delete/<id>')
# def user_delete_controller(id):
# 	#this is the controller to delete model entries
# 	user_item = User.query(User.user_id == id).get()

# 	user_item.key.delete()

# 	return 'data deletion successful <a href="/user/">back to Entries</a>'



## balance functions

# @app.route('/data/balance/')
# def data_balance():
# 	# this is the controller for JSON data access
# 	balance_list = Balance.query().fetch(10000)

# 	if balance_list:
# 		json_result = json.dumps([balance.dto() for balance in balance_list])
# 	else:
# 		json_result = None

# 	return json_result

# def get_single_balance(balance_id):
# 	balance = None
# 	single_balance = Balance.query(Balance.balance_id == balance_id).get()
# 	if single_balance:
# 		balance = single_balance.dto()
# 	result = balance
# 	return result

# @app.route('/balance/<balance_id>.json')
# def get_single_balance_json(balance_id):
# 	#this is the controller to get single entry in json format
# 	result = json.dumps(dict(balance=get_single_balance(balance_id)))
# 	return result

# @app.route('/balance/<balance_id>')
# def view_single_balance(balance_id):
# 	#this is the controller to get single entry view
# 	balance = get_single_balance(balance_id)
# 	return render_template(balance_view.html, balance = balance)

# @app.route('/balance/add/')
# def balance_add_controller():
# 	#this is the controller to add new model entries
# 	return render_template('balance_add.html', title = "Add New Entry")

# @app.route('/balance/create/',methods=['POST','GET'])
# def balance_create_data_controller():
# 	# this is the balance data create handler
# 	payee = request.values.get('payee')
# 	payer = request.values.get('payer')
# 	amount = request.values.get('amount')
# 	balance_new_id = generate_key()

# 	new_balance = Balance(
# 									balance_id = balance_new_id,
# 									payee = payee,
# 									payer = payer,
# 									amount = amount
# 								)

# 	new_balance.put()

# 	return 'data input successful <a href="/balance/">back to Entries</a>'

# @app.route('/balance/edit/<id>')
# def balance_edit_controller(id):
# 	#this is the controller to edit model entries
# 	balance_item = Balance.query(Balance.balance_id == id).get()
# 	return render_template('balance_edit.html', balance_item = balance_item, title = "Edit Entries")

# @app.route('/balance/update/<id>',methods=['POST','GET'])
# def balance_update_data_controller(id):
# 	# this is the balance data update handler
# 	payee = request.values.get('payee')
# 	payer = request.values.get('payer')
# 	amount = request.values.get('amount')
# 	balance_item = Balance.query(Balance.balance_id == id).get()
# 	balance_item.payee = payee
# 	balance_item.payer = payer
# 	balance_item.amount = amount

# 	Balance.put(balance_item)

# 	return 'data update successful <a href="/balance/">back to Entries</a>'

# @app.route('/balance/delete/<id>')
# def balance_delete_controller(id):
# 	#this is the controller to delete model entries
# 	balance_item = Balance.query(Balance.balance_id == id).get()

# 	balance_item.key.delete()

# 	return 'data deletion successful <a href="/balance/">back to Entries</a>'



## transaction functions

# @app.route('/data/transactions/')
# def data_transactions():
# 	# this is the controller for JSON data access
# 	transactions_list = Transactions.query().fetch(10000)

# 	if transactions_list:
# 		json_result = json.dumps([transactions.dto() for transactions in transactions_list])
# 	else:
# 		json_result = None

# 	return json_result

# def get_single_transactions(transactions_id):
# 	transactions = None
# 	single_transactions = Transactions.query(Transactions.transactions_id == transactions_id).get()
# 	if single_transactions:
# 		transactions = single_transactions.dto()
# 	result = transactions
# 	return result

# @app.route('/transactions/<transactions_id>.json')
# def get_single_transactions_json(transactions_id):
# 	#this is the controller to get single entry in json format
# 	result = json.dumps(dict(transactions=get_single_transactions(transactions_id)))
# 	return result

# @app.route('/transactions/<transactions_id>')
# def view_single_transactions(transactions_id):
# 	#this is the controller to get single entry view
# 	transactions = get_single_transactions(transactions_id)
# 	return render_template(transactions_view.html, transactions = transactions)

# @app.route('/transactions/edit/<id>')
# def transactions_edit_controller(id):
# 	#this is the controller to edit model entries
# 	transactions_item = Transactions.query(Transactions.transactions_id == id).get()
# 	return render_template('transactions_edit.html', transactions_item = transactions_item, title = "Edit Entries")

# @app.route('/transactions/update/<id>',methods=['POST','GET'])
# def transactions_update_data_controller(id):
# 	# this is the transactions data update handler
# 	amount = request.values.get('amount')
# 	payee = request.values.get('payee')
# 	payer = request.values.get('payer')
# 	description = request.values.get('description')
# 	transaction_time = request.values.get('transaction_time')
# 	transactions_item = Transactions.query(Transactions.transactions_id == id).get()
# 	transactions_item.amount = amount
# 	transactions_item.payee = payee
# 	transactions_item.payer = payer
# 	transactions_item.description = description
# 	transactions_item.transaction_time = transaction_time

# 	Transactions.put(transactions_item)

# 	return 'data update successful <a href="/transactions/">back to Entries</a>'

# @app.route('/transactions/delete/<id>')
# def transactions_delete_controller(id):
# 	#this is the controller to delete model entries
# 	transactions_item = Transactions.query(Transactions.transactions_id == id).get()

# 	transactions_item.key.delete()

# 	return 'data deletion successful <a href="/transactions/">back to Entries</a>'
