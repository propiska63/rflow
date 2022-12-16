from rflow.utils.petrovich.main import Petrovich
from rflow.utils.petrovich.enums import Case, Gender
import frappe
from frappe.utils import getdate
from rflow.utils.ru_number_to_text.num2t4ru import num2text

def square_text(square):
    # male_units = ((u'метр', u'метра', u'метров'), 'm')
    # female_units = ((u'копейка', u'копейки', u'копеек'), 'f')
    # male_units это plural-формы для единицы измерения и ее род 'm' - мужской, 'f' - женский
    return num2text(square)  # первая plural форма, мужской род

def period_text(period):
    male_units = ((u'месяц', u'месяца', u'месяцев'), 'm')
    r = num2text(period, male_units)
    space = r.rfind(' ')
    return f'{period} ({r[:space]}) {r[space+1:]}'

def money_text(money):
    male_units = ((u'рубль', u'рубля', u'рублей'), 'm')
    r = num2text(money, male_units)
    space = r.find(' руб')
    return f'{money} ({r[:space]}){r[space:]}'

def get_address(address):
    adr = list(frappe.db.get_value(
			'Address', address, ['pincode', 'city', 'address_line2',
			'address_line1']))
    return ', '.join(filter(None, adr))

def short_fio(contact):
    fio = list(frappe.db.get_value(
		'Contact', contact, ['last_name', 'first_name', 'middle_name']))
    return ''.join([fio[0], ' ', fio[1][0], '. ', fio[2][0], '.'])

def short_client_fio(contact):
    full_fio = contact.strip().split(' ')
    fio = []
    fio.append(full_fio[0])
    for i in range(1, len(full_fio)):
        fio.append(f'{full_fio[i][0]}.')
    return ' '.join(fio)

def morph_date(date, full=False):
    month = {'January': 'января',
            'Январь': 'января',
            'February': 'февраля',
            'Февраль': 'февраля',
            'March': 'марта',
            'Март': 'марта',
            'April': 'апреля',
            'May': 'мая',
            'Май': 'мая',
            'June': 'июня',
            'Июнь': 'июня',
            'July': 'июля',
            'Июль': 'июля',
            'August': 'августа',
            'Август': 'августа',
            'September': 'сентября',
            'Сентябрь': 'сентября',
            'October': 'октября',
            'Октябрь': 'октября',
            'November': 'ноября',
            'Ноябрь': 'ноября',
            'December': 'декабря'}

    date = getdate(date)
    dt = date.strftime("%d:%B:%Y").split(':')
    dt[1] = month[dt[1]]
    if full:
        dt.append('года')
    else:
        dt.append('г.')
    return ' '.join(dt)

def morph_fio(fullname):
    fio = []
    fio = fullname.strip().split(' ')
    p = Petrovich()
    try:
        fio[0] = (p.lastname(fio[0], Case.GENITIVE))
    except:
        pass
    try:
        fio[1] = (p.firstname(fio[1], Case.GENITIVE))
    except:
        pass
    try:
        fio[2] = (p.middlename(fio[2], Case.GENITIVE))
    except:
        pass
    return ' '.join(fio)

def morph_contact_fio(contact):
    fio = []
    cont = frappe.get_doc('Contact', contact)
    p = Petrovich()
    try:
        fio.append(p.lastname(cont.last_name, Case.GENITIVE))
    except:
        pass
    try:
        fio.append(p.firstname(cont.first_name, Case.GENITIVE))
    except:
        pass
    try:
        fio.append(p.middlename(cont.middle_name, Case.GENITIVE))
    except:
        pass
    return ' '.join(fio)

def morph_director(fullname):
    director = fullname.strip().split(' ')
    if director[0].lower == 'председатель':
        director[0] = 'Председателя'
    else:
        p = Petrovich()
        director[0] = p.lastname(director[0], Case.GENITIVE, Gender.MALE)
        if len(director)>1:
            director[1] = p.firstname(director[1], Case.GENITIVE, Gender.MALE)
    return ' '.join(director)

def get_signature(company):
    doc = frappe.get_doc('OurCompany', company)
    if doc.signature:
        return frappe.db.get_value('File', {'attached_to_doctype': 'OurCompany','attached_to_name': doc.name}, 'file_url')
    else:
        return ''

def get_city(address):
    return frappe.get_value('Address', address, 'city')
