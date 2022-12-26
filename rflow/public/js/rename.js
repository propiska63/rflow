let rename_document = (frm, input_name) => {
    const docname = frm.doc.name;
	const doctype = frm.doctype;
    return frappe
            .xcall("frappe.model.rename_doc.update_document_title", {
                doctype,
                docname,
                name: input_name,
                enqueue: false,
                merge: false,
                freeze: true,
                freeze_message: __("Updating related fields..."),
            })
            .then((new_docname) => {
                const reload_form = (input_name) => {
                    $(document).trigger("rename", [doctype, docname, input_name]);
                    if (locals[doctype] && locals[doctype][docname]) {
                        //delete locals[doctype];
                        delete locals[doctype][docname];
                        frappe.ui.toolbar.clear_cache()
                    }
                    //frm.reload_doc();
                    
                };

                // handle document renaming queued action
                if (input_name && new_docname == docname) {
                    frappe.socketio.doc_subscribe(doctype, input_name);
                    frappe.realtime.on("doc_update", (data) => {
                        if (data.doctype == doctype && data.name == input_name) {
                            reload_form(input_name);
                            //frappe.ui.toolbar.clear_cache()

                            frappe.show_alert({
                                message: __("Document renamed from {0} to {1}", [
                                    docname.bold(),
                                    new_docname.bold(),
                                ]),
                                indicator: "success",
                            });
                        }
                    });
                    frappe.show_alert(
                        __("Document renaming from {0} to {1} has been queued", [
                            docname.bold(),
                            input_name.bold(),
                        ])
                    );
                }

                // handle document sync rename action
                if (input_name && (new_docname || input_name) != docname) {
                    reload_form(new_docname || input_name);
                    //frappe.ui.toolbar.clear_cache()
                }
            });
    };