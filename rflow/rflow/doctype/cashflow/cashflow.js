// Copyright (c) 2023, Alex Kuzin and contributors
// For license information, please see license.txt


frappe.ui.form.on("CashFlow", {
// 	refresh(frm) {

// 	},
// });

onload: function(frm) {
    frm.set_query('account', () => {
        return {
        filters: {
            docstatus: 1
            }
        }
    })
    if (frm.doc.document_type) {
        frm.call('get_account', { doctype: frm.doc.document_type })
            .then(r => {
                if (r.message) {
                    frm.set_value({
                        account: r.message
                    })
                }
        })
    }
},

account: function(frm) {
    if (frm.doc.document && frm.doc.account) {
        frm.call('check_account', { account: frm.doc.account, docname: frm.doc.document})
            .then(r => {
                if (!r.message) {
                    frm.set_value({
                        document: null
                    })
                }
        })
    }
}

})
