# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils import getdate
from frappe.utils import add_to_date
from frappe import _, throw
import datetime
import rflow.utils.morph as morph

class RieltFlow(Document):

	@frappe.whitelist()
	def get_tax_area(self, throw_if_missing=False):
		if not frappe.db.exists('CheckerBoard', self.address):
			if throw_if_missing:
				throw(_('Error - Linked address not found'))

		return frappe.get_doc('CheckerBoard', self.address)
	# Compose unique name
	def autoname(self):
		self.name = cstr(f'{self.company} | {self.address}')
		if frappe.db.exists("RieltFlow", self.name):
			self.name = cstr(f'{self.name} #{getseries(self.name, 1)}')
	def before_save(self):
		# Set week of record
		weekday = getdate(self.date).weekday()
		monday = add_to_date(getdate(self.date), days=-weekday).strftime('%d.%m.%y')
		satuday = add_to_date(getdate(self.date), days=6-weekday).strftime('%d.%m.%y')
		self.week = f'{monday}-{satuday}'

		# Set exp_date
		if self.registration_date:
			self.exp_date = add_to_date(self.registration_date, months=self.period)
			self.exp_month = f'{morph.russian_month(getdate(self.exp_date).strftime("%B"))} {getdate(self.exp_date).strftime("%Y")}'
		else:
			self.exp_date = None
			self.exp_month = None

		if len(self.director.strip().split(' ')) < 3:
				throw(_('Please enter full director FIO'))
	def before_submit(self):
		if not frappe.db.exists('CheckerBoard', self.address):
				throw(_('Error - Linked address not found'))
		checker = frappe.get_doc('CheckerBoard', self.address)
		if checker.docstatus == 0:
			checker._submit()
	def on_update(self):
		# Set CheckerBoard link for filters
		if self.address:
			frappe.db.set_value('CheckerBoard', self.address, 'rielt_flow', self.name)
		old = self.get_doc_before_save()
		if not old:
			return
		else:
			if old.address != self.address and old.address:
				frappe.db.set_value('CheckerBoard', old.address, 'rielt_flow', None)


	def on_update_after_submit(self):
		if self.registration_date:
			self.exp_date = add_to_date(self.registration_date, months=self.period)
			self.exp_month = f'{morph.russian_month(getdate(self.exp_date).strftime("%B"))} {getdate(self.exp_date).strftime("%Y")}'
		else:
			self.exp_date = None
			self.exp_month = None

	def on_trash(self):
		if self.address and not self.deal_name:
			frappe.db.set_value('CheckerBoard', self.address, 'rielt_flow', None)
