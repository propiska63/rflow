import frappe
from frappe.contacts.doctype.address.address import Address
from frappe.model.naming import make_autoname
from frappe.utils import cstr
from frappe import _, throw

class RFlowAddress(Address):
	def autoname(self):
		if not self.address_title:
			if self.links:
				self.address_title = self.links[0].link_name

		if self.address_title:
			self.name = cstr(self.address_title).strip()
			if frappe.db.exists("Address", self.name):
				self.name = make_autoname(
					cstr(self.address_title).strip() + "-.#"
				)
		else:
			throw(_("Address Title is mandatory."))
