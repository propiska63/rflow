// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('OurCompany', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
		frm.set_query('company_address', () => {
			return {
			filters: {
			disabled: 0,
			address_type: __('Office')
			}
			}
		})
	}
})
