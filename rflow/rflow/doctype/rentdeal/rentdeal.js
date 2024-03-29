// Copyright (c) 2022, Alex Kuzin and contributors
// For license information, please see license.txt

frappe.ui.form.on('RentDeal', {
	refresh: function(frm) {
		if (!frm.is_new()) {
		frm.add_custom_button(__("Payments"), function() {
			if (frm.is_dirty()) {
				frappe.confirm(__('Save Rent Deal and go to CashFlow list?'),
    			() => {
        		// action to perform if Yes is selected
				frm.save();
				frappe.set_route("List", "CashFlow", {"document_type": 'RentDeal',"document": frm.doc.name});
    			})
			} else {
				frappe.set_route("List", "CashFlow", {"document_type": 'RentDeal',"document": frm.doc.name});
			}})}		
	},
	onload: function(frm) {
		if (frm.doc.guarantee_letter) {
			frm.doc.guarantee = 1;
		}
		let guarantee = frm.doc.guarantee;
		frm.toggle_display(['guarantee_letter'], guarantee === 1);
		frm.toggle_display(['registration'], guarantee === 0);
		frm.toggle_enable(['contact','individual','pay_first','address','date'],
			guarantee === 0);


		if (guarantee === 1) {
			frm.set_df_property('date', 'label', __('Registration Date'))
		}
		else {
			frm.set_df_property('date', 'label', __('Date'))
		}

		let individual = frm.doc.individual;
		frm.toggle_display(['passport','issued_by','when_iissued'],
			individual === 1);
		if (individual === 1) {
			frm.set_df_property('registration', 'label', __('Registration'))
		}
		else {
			frm.set_df_property('registration', 'label', __('Company Address'))
		}

		frm.toggle_display([
			'company_type','director','inn','ogrn','kpp','bank','account','bik','cor_account'],
			individual === 0);
		frm.toggle_reqd(['company_type','director','inn','ogrn','kpp'],
			individual === 0);
		frm.set_query('guarantee_letter', () => {
			return {
			filters: {
			docstatus: 1,
			deal_name: ''
			}
			}
		});
		frm.set_query('address', () => {
			return {
			filters: {
			rent_deal: '',
			rielt_flow: ''
			}
			}
		});
	},
	address: function(frm) {
		if (frm.doc.guarantee === 0 && frm.doc.address) {
			frm.call('get_checker', { throw_if_missing: true })
    			.then(r => {
        			if (r.message) {
            			let linked_doc = r.message;
            			// do something with linked_doc
						frm.set_value({
							price: linked_doc.price,
						})
        			}
    		})
		}
	},
	guarantee: function(frm) {
		let guarantee = frm.doc.guarantee;
		frm.toggle_display(['guarantee_letter'], guarantee === 1);
		frm.toggle_display(['registration'], guarantee === 0);
		frm.toggle_enable(['contact','individual','pay_first','address','date'],
			guarantee === 0);
		frm.set_value({
			date: null,
			address: null,
			paid_to: null,
			contact: null,
			guarantee_letter: null,
			exp_date: null
		})
		if (guarantee === 1) {
			frm.set_df_property('date', 'label', __('Registration Date'))
			frm.set_value({
				individual: 0,
				pay_first: 0,
			})
		}
		else {
			frm.set_df_property('date', 'label', __('Date'))
		}
	},
	guarantee_letter: function(frm) {
		if (frm.doc.guarantee_letter && frm.doc.guarantee === 1) {
			frm.call('get_linked_flow', { throw_if_missing: true })
    			.then(r => {
        			if (r.message) {
            				let linked_doc = r.message[0];
							let paid_to = r.message[1];
            				// do something with linked_doc
					frm.set_value({
						date: linked_doc.registration_date,
						address: linked_doc.address,
						contact: linked_doc.agent,
						price: linked_doc.revenue / linked_doc.period,
						company: linked_doc.company,
						company_type: linked_doc.company_type,
						director: linked_doc.director,
						inn: linked_doc.inn,
						ogrn: linked_doc.ogrn,
						kpp: linked_doc.kpp,
						pledge: '0%',
						paid_to: paid_to
					})

        			}
    		})
		}
	},
	individual: function(frm) {
		let individual = frm.doc.individual;
		frm.toggle_display(['passport','issued_by','when_iissued'],
			individual === 1);
		if (individual === 1) {
			frm.set_df_property('registration', 'label', __('Registration'))
		}
		else {
			frm.set_df_property('registration', 'label', __('Company Address'))
		}

		frm.toggle_display([
			'company_type','director','inn','ogrn','kpp','bank','account','bik','cor_account'],
			individual === 0);
		frm.toggle_reqd(['company_type','director','inn','ogrn','kpp'],
			individual === 0);
		if (individual === 1) {
			frm.set_df_property('company', 'label', __('Tenant Name'));
			frm.set_value({
				company_type: '',
				director: '',
				inn: '',
				ogrn: '',
				kpp: '',
				bank: '',
				account: '',
				bik: '',
				cor_account: ''
			})
		}
		else {
			frm.set_df_property('company', 'label', __('Company Name'));
			frm.set_value({
				registration: '',
				passport: '',
				issued_by: '',
				when_iissued: ''
			})
		}


	}
});
