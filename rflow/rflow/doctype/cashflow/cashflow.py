# Copyright (c) 2023, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils import cstr
from frappe import _, throw

class CashFlow(Document):
	@frappe.whitelist()
	def get_account(self, doctype):
		# Get all master accounts of selected doctype
		accounts = frappe.db.get_list('CashAccount',
		filters={
			'linked_documents': doctype,
			'master_account': 1
    	},
    	fields='name',
    	as_list=True)
		try:
			return accounts[0][0]
		except IndexError:
			return False
	
	@frappe.whitelist()
	def check_account(self, account, docname):
		# Get account doctype
		type = frappe.db.get_value('CashAccount', account, 'linked_documents')
		return True if frappe.db.exists(type, docname) else False

	#  Compose unique name
	def get_name(self):
		account = frappe.db.get_value('CashAccount', self.account, 'account_name')
		return cstr(f'{account} | {self.date}')
	def autoname(self):
		self.name = self.get_name()
		#if frappe.db.exists("CashFlow", self.name):
		self.name = f'{self.name} | {getseries(self.name, 1)}'
	
	def before_save(self):
		account = frappe.get_doc('CashAccount', self.account)
		if self.rate > 0 and not account.enable_income_operations: self.rate = self.rate * -1
		elif self.rate < 0 and not account.enable_expense_operations: self.rate = self.rate * -1

	def before_submit(self):
		if self.document:
			if not frappe.db.exists(self.document_type, self.document):
				throw(_('Error - Linked document not found'))
			match self.document_type:
				case 'RieltFlow':
					address = frappe.get_value('RieltFlow',self.document,'address')
					self.ownerdeal = frappe.get_value('CheckerBoard', address,'address')
					#frappe.msgprint(f'Set RieltFlow address {self.ownerdeal}')
				case "RentDeal":
					address = frappe.get_value('RentDeal',self.document,'address')
					self.ownerdeal = frappe.get_value('CheckerBoard', address,'address')
				case "OwnerDeal":
					self.ownerdeal = self.document