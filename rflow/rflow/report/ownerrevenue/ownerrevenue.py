# Copyright (c) 2023, Alex Kuzin and contributors
# For license information, please see license.txt

import frappe
from frappe import _

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU')
#"holiday_date": ["between", (self.start_date, self.end_date)],

def execute(filters=None):
	columns = get_columns(filters)
	letters, sum_letters = add_total_row(get_data(filters, 'RieltFlow'), _('Total Letter Revenue'))
	rent, sum_rent = add_total_row(get_data(filters, 'RentDeal'), _('Total Rent Revenue'))
	expenses, sum_expenses = add_total_row(get_data(filters, 'OwnerDeal'), _('Total Expenses'))
	total = add_total([sum_letters,sum_rent,sum_expenses],filters)

	data = []
	data.extend(letters)
	data.extend(rent)
	data.extend(expenses)
	data.extend(total)

	return columns, data

def get_columns(filters):
	return [
		_('Date') + ':Date:120',
		_('CashAccount') + ':Data:250',
		_('Document') + ':Data:300',
		_('Sum') + ':Data:100',
		]

def money(value):
	return locale.currency(value, symbol=False, grouping=True)

def add_total(accounts, filters, description=None, owner_description=None, managment_description=None):
	# Calculate sum and owner revenue
	summary = sum(accounts)
	if not description: description = _('Total Revenue')
	if not owner_description: owner_description = _('Total Owner Revenue')
	if not managment_description: managment_description = _('Managment comission')
	rows = []
	rows.append(['','',f'<div style align=right><b>{description}:</b></div>',f'<div style align=right><b>{money(summary)}</b></div>'])
	# Get procentil of Owner Revenue
	if filters.get('ownerdeal'):
		percent = frappe.db.get_value('OwnerDeal', filters['ownerdeal'], 'owner_percentage')
		sheet = _('Calculation: income - expenses - managment')
		rows.append(['','',f'<div style align=right><b>{managment_description}:</b><br><i>{sheet}<i></div>',f'<div style align=right><b>{percent}%</b></div>'])
		#rows.append(['','',f'<div style align=right>{sheet}</div>',''])
		rows.append(['','',f'<div style align=right><h4><b>{owner_description}:</b></h4></div>',f'<div style align=right><h4><b>{money(summary * percent / 100)}</b></h4></div>'])
	return rows

def add_total_row(rows, description=None):
	ret = []
	sum = 0.00
	if rows:
		if not description: description = _('Total')
		for row in rows:
			row = list(row)
			sum += row[3]
			row[3] = f'<div style align=right>{money(row[3])}</div>'
			ret.append(row)

		ret.append(['','',f'<div style align=right><b>{description}:</b></div>',f'<div style align=right><b>{money(sum)}</b></div>'])
		ret.append(['','','',''])
#	rows.append(['','','<div style align=right><b>Итого:</b></div>',locale.currency(sum, symbol=True, grouping=True)])

	return ret, sum

def get_data(filters, doctype=None):
	conditions=get_conditions(filters, doctype)
#	query = frappe.db.sql(
#		"""
#		select date, account, document, rate from tabCashFlow 
#		where {cond} order by date""".format(cond=conditions), filters, as_dict=0)
	query = frappe.db.sql(
		"""
		SELECT date, account, document, rate 
		FROM tabCashFlow cf LEFT JOIN tabCashAccount acc ON cf.account = acc.name
		WHERE {cond} ORDER BY date""".format(cond=conditions), filters, as_dict=0)
	return list(query)

def get_conditions(filters, doctype=None):
	#conditions = 'include_in_reports = 1'
	conditions = 'acc.include_in_reports = 1 and cf.docstatus = 1'
	if doctype: conditions += f" and cf.document_type = '{doctype}'"
	if filters.get("ownerdeal"): conditions += ' and cf.ownerdeal = %(ownerdeal)s'
	if filters.get("start_date"): conditions += ' and cf.date >= %(start_date)s'
	if filters.get("end_date"): conditions += ' and cf.date <= %(end_date)s'
	return conditions