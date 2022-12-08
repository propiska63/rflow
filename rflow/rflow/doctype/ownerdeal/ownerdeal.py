# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_abbr
from frappe.utils import getdate
from frappe.utils import add_to_date
from frappe.model.naming import getseries
from frappe.model.naming import make_autoname
from frappe.utils import cstr
from frappe import _, throw


class OwnerDeal(Document):
	def autoname(self):
		self.name = self.address
		if frappe.db.exists("OwnerDeal", self.name):
			self.name = cstr(f'{self.name} {getseries(self.name, 1)}')

	def before_cancel(self):
		self.in_use = False

	def before_save(self):
		if not self.prefix:
			self.prefix = get_abbr(self.address)

		# Set exp_date
		if self.deal_date and self.deal_period:
			self.exp_date = add_to_date(self.deal_date, months=self.deal_period)
			self.exp_month = getdate(self.exp_date).strftime("%B %Y")
		else:
			self.exp_date = ''
			self.exp_month = ''
		# Set area of deal from TaxCode table
		self.taxarea = frappe.db.get_value('TaxCode', self.tax_code, 'area')

	def on_update(self):
		# Set contact as active
		frappe.db.set_value('Contact', self.contact, 'status', 'Open')
