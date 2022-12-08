// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('OwnerDeal', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
		frm.set_query('address', () => {
			return {
			filters: {
			disabled: 0,
			address_type: __('Current')
			}
			}
		})
		frm.set_query('our_company', () => {
			return {
			filters: {
			docstatus: 1,
			}
			}
		})
	}
})