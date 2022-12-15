# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _, throw
from frappe.utils import add_to_date
from frappe.utils import getdate
from frappe.utils import get_abbr
from frappe.utils import cstr
import datetime

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

class RentDeal(Document):

	@frappe.whitelist()
	def get_linked_flow(self, throw_if_missing=False):
		if not frappe.db.exists('RieltFlow', self.guarantee_letter):
			if throw_if_missing:
				throw(_('Error - Linked guarantee letter not found'))

		return frappe.get_doc('RieltFlow', self.guarantee_letter)

	@frappe.whitelist()
	def get_checker(self, throw_if_missing=False):
		if not frappe.db.exists('CheckerBoard', self.address):
			if throw_if_missing:
				throw(_('Error - Linked checkerboard record not found'))

		return frappe.get_doc('CheckerBoard', self.address)

	def autoname(self):
		# Compose unique dial number
		year = datetime.date.today().year
		ownerdeal, office, place = frappe.db.get_value('CheckerBoard', self.address, ['address', 'office', 'place'])
		prefix, address = frappe.db.get_value('OwnerDeal', ownerdeal, ['prefix', 'address'])
		possession = frappe.db.get_value('Address', address, 'address_line1').split(' ')[1] or '00'
		if office:
			if place:
				object = cstr(f'{office}.{place}')
			else:
				object = cstr(office)
			#self.deal_name = cstr(f'{possession}-{object}/{prefix}-{getdate(self.date).year}')
			self.deal_name = cstr(f'{possession}-{object}/{prefix}')

			#self.name = f'{self.company} {self.deal_name} {self.date}'
		else:
			#self.deal_name = cstr(f'{possession}/{prefix}-{datetime.date.today().year}')
			self.deal_name = cstr(f'{possession}/{prefix}')

		self.name = f'{self.company} {self.deal_name} {self.date}'

	def before_save(self):
		# Set exp_date
		if self.date and self.rent_period:
			self.exp_date = add_to_date(self.date, months=self.rent_period)
			self.exp_month = f'{russian_month(getdate(self.exp_date).strftime("%B"))} {getdate(self.exp_date).strftime("%Y")}'
		else:
			self.exp_date = None
			self.exp_month = None
	
	def before_submit(self):
		if not frappe.db.exists('CheckerBoard', self.address):
				throw(_('Error - Linked address not found'))
		checker = frappe.get_doc('CheckerBoard', self.address)
		if checker.docstatus == 0:
			checker._submit()
		if not frappe.db.exists('RieltFlow', self.guarantee_letter):
			throw(_('Error - Linked guarantee letter not found'))
		rflow = frappe.get_doc('RieltFlow', self.guarantee_letter)
		if rflow.docstatus == 0:
			rflow._submit()
	
	def on_update(self):
		# Set CheckerBoard link for filters
		if self.address:
			frappe.db.set_value('CheckerBoard', self.address, 'rent_deal', self.name)
		if self.guarantee_letter:
			frappe.db.set_value('RieltFlow', self.guarantee_letter, 'deal_name', self.name)
			#frappe.db.set_value('RieltFlow', self.guarantee_letter, 'docstatus', 1)
		old = self.get_doc_before_save()
		if not old:
			return

		if old.address != self.address and old.address:
			frappe.db.set_value('CheckerBoard', old.address, 'rent_deal', None)

		if old.guarantee_letter != self.guarantee_letter and old.guarantee_letter:
			frappe.db.set_value('RieltFlow', old.guarantee_letter, 'deal_name', None)

	def on_trash(self):
		if self.address:
			frappe.db.set_value('CheckerBoard', self.address, 'rent_deal', '')
		if self.guarantee:
			frappe.db.set_value('RieltFlow', self.guarantee_letter, 'deal_name', None)

	def before_cancel(self):
		if self.address:
			frappe.db.set_value('CheckerBoard', self.address, 'rent_deal', None)
		if self.guarantee:
			frappe.db.set_value('RieltFlow', self.guarantee_letter, 'deal_name', None)
