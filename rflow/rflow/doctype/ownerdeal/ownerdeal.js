// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('OwnerDeal', {
	refresh: function(frm) {
		if (!frm.is_new()) {
		frm.add_custom_button(__("CheckerBoard"), function() {
			if (frm.is_dirty()) {
				frappe.confirm(__('Save Owner Deal and go to CheckerBoard list?'),
				() => {
				// action to perform if Yes is selected
				frm.save();
				frappe.set_route("List", "CheckerBoard", {"address": frm.doc.name});
				})
			} else {
				frappe.set_route("List", "CheckerBoard", {"address": frm.doc.name});
			}});
		frm.add_custom_button(__("Payments"), function() {
			if (frm.is_dirty()) {
				frappe.confirm(__('Save Owner Deal and go to CashFlow list?'),
    			() => {
        		// action to perform if Yes is selected
				frm.save();
				frappe.set_route("List", "CashFlow", {"ownerdeal": frm.doc.name});
    			})
			} else {
				frappe.set_route("List", "CashFlow", {"ownerdeal": frm.doc.name});
			}});
		}		
	},
	onload: function(frm) {
		frm.set_query('address', () => {
			return {
			filters: {
			disabled: 0,
			address_type: 'Current'
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