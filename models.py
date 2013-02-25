# coding: UTF-8
##############################################
# models.py - ndb model definition file		 #
# the datastore implemented is ndb			 #
# this is due to performance considerations  #
##############################################
from google.appengine.ext import ndb
from helpers import thousand_separator

class User(ndb.Model):
	user_id = ndb.StringProperty()
	email = ndb.StringProperty()
	firstname = ndb.StringProperty()
	lastname = ndb.StringProperty()
	password = ndb.StringProperty()
	join_date = ndb.DateTimeProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				user_id = self.user_id,
				email = self.email,
				firstname = self.firstname,
				lastname = self.lastname,
				join_date = self.join_date.isoformat())

class Balance(ndb.Model):
	balance_id = ndb.StringProperty()
	payee = ndb.StringProperty()
	payer = ndb.StringProperty()
	amount = ndb.FloatProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				balance_id = self.balance_id,
				payee = self.payee,
				payer = self.payer,
				amount = thousand_separator(int(self.amount)))

class Transactions(ndb.Model):
	transactions_id = ndb.StringProperty()
	amount = ndb.FloatProperty()
	payee = ndb.StringProperty()
	payer = ndb.StringProperty()
	description = ndb.StringProperty()
	transaction_time = ndb.DateTimeProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				transactions_id = self.transactions_id,
				amount = thousand_separator(int(self.amount)),
				payee = self.payee,
				payer = self.payer,
				description = self.description,
				transaction_time = self.transaction_time.isoformat())
