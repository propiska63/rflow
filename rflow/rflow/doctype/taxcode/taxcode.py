# Copyright (c) 2022, Alex Kuzin and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class TaxCode(Document):
	def autoname(self):
		self.name = self.taxcode
