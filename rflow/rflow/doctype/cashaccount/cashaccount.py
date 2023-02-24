# Copyright (c) 2023, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils import cstr

class CashAccount(Document):
	# Compose unique name
	def get_name(self):
		return cstr(f'{self.account_code} | {self.account_name}')
	def autoname(self):
		self.name = self.get_name()
		if frappe.db.exists("CashAccount", self.name):
			self.name = f'{self.name} #{getseries(self.name, 1)}'
