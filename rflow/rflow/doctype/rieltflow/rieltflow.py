# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cstr
from frappe.model.document import Document
from frappe.model.naming import getseries
from frappe.utils import getdate
from frappe.utils import add_to_date
from frappe import _, throw

def russian_month(date):
    month = {'January': 'Январь',
            'February': 'Февраль',
            'March': 'Март',
            'April': 'Апрель',
            'May': 'Май',
            'June': 'Июнь',
            'July': 'Июль',
            'August': 'Август',
            'September': 'Сентябрь',
            'October': 'октября',
            'Октябрь': 'Октябрь',
            'November': 'Ноябрь',
            'December': 'Декабрь'}
    return month[date]

class RieltFlow(Document):

	@frappe.whitelist()
	def get_tax_area(self, throw_if_missing=False):
		if not frappe.db.exists('CheckerBoard', self.address):
			if throw_if_missing:
				throw(_('Error - Linked address not found'))

		return frappe.get_doc('CheckerBoard', self.address)

	@frappe.whitelist()
	def need_rename(self):
		name = self.get_name()
		if not name in self.name:
			if frappe.db.exists("RieltFlow", name):
				name = f'{name} #{getseries(name, 1)}'
			return name
		return False

	def get_exp_date(self):
		if self.registration_date:
			self.exp_date = add_to_date(self.registration_date, months=self.period)
			self.exp_month = f'{russian_month(getdate(self.exp_date).strftime("%B"))} {getdate(self.exp_date).strftime("%Y")}'
		else:
			self.exp_date = None
			self.exp_month = None

	# Compose unique name
	def get_name(self):
		return cstr(f'{self.company} | {self.address}')
	def autoname(self):
		self.name = self.get_name()
		if frappe.db.exists("RieltFlow", self.name):
			self.name = f'{self.name} #{getseries(self.name, 1)}'
		
	def before_save(self):
		# Set week of record
		weekday = getdate(self.date).weekday()
		monday = add_to_date(getdate(self.date), days=-weekday).strftime('%d.%m.%y')
		satuday = add_to_date(getdate(self.date), days=6-weekday).strftime('%d.%m.%y')
		self.week = f'{monday}-{satuday}'

		# Set exp_date
		self.get_exp_date()

		if len(self.director.strip().split(' ')) < 3:
				throw(_('Please enter full director FIO'))

	def before_submit(self):
		self.get_exp_date()
		if not frappe.db.exists('CheckerBoard', self.address):
				throw(_('Error - Linked address not found'))
		checker = frappe.get_doc('CheckerBoard', self.address)
		if checker.docstatus == 0:
			checker._submit()

	def on_update(self):
		self.get_exp_date()

		# Set CheckerBoard link for filters
		if self.address:
			frappe.db.set_value('CheckerBoard', self.address, 'rielt_flow', self.name)
		old = self.get_doc_before_save()
		if not old:
			return
		else:
			if old.address != self.address and old.address:
				frappe.db.set_value('CheckerBoard', old.address, 'rielt_flow', None)

	def before_update_after_submit(self):
		self.get_exp_date()


	def on_trash(self):
		if self.address and not self.deal_name:
			frappe.db.set_value('CheckerBoard', self.address, 'rielt_flow', None)
