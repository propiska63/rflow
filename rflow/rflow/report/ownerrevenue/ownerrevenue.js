// Copyright (c) 2023, Alex Kuzin and contributors
// For license information, please see license.txt
/* eslint-disable */

var today = frappe.datetime.now_date(as_obj = false);
var prev_month = frappe.datetime.add_months(today,-1);
var start = moment(prev_month).startOf("month").format();
var end = moment(prev_month).endOf("month").format();


frappe.query_reports["OwnerRevenue"] = {
	"filters": [
		{
			"fieldname":"ownerdeal",
			"label": __("Premises"),
			"fieldtype": "Link",
			"options": "OwnerDeal",
			//"default": frappe.defaults.get_user_default("company")
		},
		{
		"fieldname":"start_date",
		"label": __("From Date"),
		"fieldtype": "Date",
		"reqd": 1,
		//"default": frappe.datetime.year_start()
		"default": start
		},
		{
		"fieldname":"end_date",
		"label": __("To Date"),
		"fieldtype": "Date",
		"reqd": 1,
		//"default": frappe.datetime.year_end()
		"default": end
		}
	]
};
