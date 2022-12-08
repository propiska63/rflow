# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.model.naming import getseries


class CheckerBoard(Document):
	def autoname(self):
		prefix = ''
		if self.office:
			prefix = ' - ' + self.office
			if self.place:
				prefix += '/' + self.place

		self.name = self.address + prefix
		if frappe.db.exists("CheckerBoard", self.name):
			self.name = cstr(f'{self.name} #{getseries(self.name, 1)}')

	def before_save(self):
		self.taxarea = frappe.db.get_value('OwnerDeal', self.address, 'taxarea')