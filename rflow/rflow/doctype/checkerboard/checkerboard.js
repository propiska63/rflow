// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('CheckerBoard', {
	setup: function(frm) {
		frm.toggle_display(['rent_flow'], self.rent_deal === '');
		frm.set_query('address', () => {
			return {
			filters: {
			docstatus: 1,
			in_use: 1
			}
			}
		})
	}
	// refresh: function(frm) {

	// }
});
