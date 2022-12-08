# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe import _, throw
from frappe.model.document import Document


class OurCompany(Document):
	def autoname(self):
		self.name = f'{self.company_name} - {self.inn}'
	def before_save(self):
		frappe.db.set_value('Contact', self.director, 'status', 'Open')

		# Check full director's name
		fio = list(frappe.db.get_value(
			'Contact', self.director, ['last_name', 'first_name', 'middle_name']))
		if len(fio) < 3:
			throw(
				title=_('Error'),
				msg=_('Please set direcor\'s last and middle name'))

		self.sign = self.signature


