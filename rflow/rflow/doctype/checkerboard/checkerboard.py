# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.model.naming import getseries
from frappe import _, throw


class CheckerBoard(Document):
	@frappe.whitelist()
	def get_linked_address(self, throw_if_missing=False):
		if not frappe.db.exists('OwnerDeal', self.address):
			if throw_if_missing:
				throw(_('Error - Linked address not found'))
		doc = frappe.get_doc('OwnerDeal', self.address)

		values = {'address': f'{self.address}'}
		data = frappe.db.sql("""
    		SELECT
				checker.address,
        		checker.office,
        		checker.place
    		FROM `tabCheckerBoard` checker
    		WHERE checker.address = %(address)s and checker.office = ( SELECT MAX(office) FROM `tabCheckerBoard` )
			ORDER BY checker.place DESC
			LIMIT 1
			""", values=values, as_dict=1)
		if int(data[0]['place']) > 2:
			self.office = int(data[0]['office']) + 1
			self.place = 1
		else:
			self.office = int(data[0]['office'])
			self.place = int(data[0]['place']) + 1
		self.price = doc.default_price
		return self

	def autoname(self):
		prefix = ''
		if self.office:
			prefix = ' - ' + str(self.office)
			if self.place:
				prefix += '/' + str(self.place)

		self.name = self.address + prefix
		if frappe.db.exists("CheckerBoard", self.name):
			self.name = cstr(f'{self.name} #{getseries(self.name, 1)}')

	def before_save(self):
		self.taxarea = frappe.db.get_value('OwnerDeal', self.address, 'taxarea')
	