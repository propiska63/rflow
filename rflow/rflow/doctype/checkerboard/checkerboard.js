// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('CheckerBoard', {
	setup: function(frm) {
		frm.toggle_display(['rielt_flow'], self.rent_deal === '');
		frm.set_query('address', () => {
			return {
			filters: {
			docstatus: 1,
			in_use: 1
			}
			}
		})
	},
	address: function(frm) {
		if (frm.doc.address) {
			frm.call('get_linked_address', { throw_if_missing: true })
    			.then(r => {
        			if (r.message) {
            				let linked_doc = r.message;
            				// do something with linked_doc
					frm.set_value({
						price: linked_doc.price,
						office: linked_doc.office,
						place: linked_doc.place
					})

        			}
    		})
		}
	},
});
