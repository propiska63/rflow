// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('RieltFlow', {

	onload: function(frm) {
		frm.set_query('address', () => {
			return {
			filters: {
				//taxarea: frm.doc.tax_area,
				rielt_flow: '',
				rent_deal: ''
				}
			}
		})
		frm.set_query('agent', () => {
			return {
			filters: {
				status: 'Open'
				}
			}
		})
	},
	address: function(frm) {
		if (frm.doc.address) {
			frm.call('get_tax_area', { throw_if_missing: true })
    			.then(r => {
        			if (r.message) {
            				let linked_doc = r.message;
            				// do something with linked_doc
					frm.set_value({
						tax_area: linked_doc.taxarea
					});
        			}
				})
			}
	},
	tax_area: function(frm) {
		if (frm.doc.tax_area && frm.doc.address) {
			frm.call('get_tax_area', { throw_if_missing: true })
    			.then(r => {
        			if (r.message) {
            				let linked_doc = r.message;
            				// do something with linked_doc
					if (frm.doc.tax_area !== linked_doc.taxarea) {
						frm.set_value('address', '')
					}
					frm.set_query('address', () => {
						return {
						filters: {
							taxarea: frm.doc.tax_area,
							rielt_flow: '',
							rent_deal: ''
							}
						}
					})
				}
			});
		} else if (!frm.doc.tax_area) {
			frm.set_query('address', () => {
				return {
				filters: {
					//taxarea: frm.doc.tax_area,
					rielt_flow: '',
					rent_deal: ''
					}
				}
			})
		} else {
			frm.set_query('address', () => {
				return {
				filters: {
					taxarea: frm.doc.tax_area,
					rielt_flow: '',
					rent_deal: ''
					}
				}
			})
		}
	}
})
