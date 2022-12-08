
import datetime
from rflow.utils.petrovich.main import Petrovich
from rflow.utils.petrovich.enums import Case, Gender
import frappe

@frappe.whitelist()
def russian_month(date):
    month = {'January': 'Январь',
            'February': 'Февраль',
            'March': 'Март',
            'April': 'Апрель',
            'May': 'Май',
            'June': 'Июнь',
            'July': 'Июль',
            'August': 'Август',
            'September': 'Сентябрь',
            'October': 'октября',
            'Октябрь': 'Октябрь',
            'November': 'Ноябрь',
            'December': 'Декабрь'}
    return month[date]

def date(date, full=False):
    month = {'January': 'января',
            'Январь': 'января',
            'February': 'февраля',
            'Февраль': 'февраля',
            'March': 'марта',
            'Март': 'марта',
            'April': 'апреля',
            'Апрель': 'апреля',
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
            'December': 'декабря',
            'Декабрь': 'декабря'}
    dt = date.strftime("%d:%B:%Y").split(':')
    dt[1] = month[dt[1]]
    if full:
        dt.append('года')
    else:
        dt.append('г.')
    return ' '.join(dt)

@frappe.whitelist()
def fio(fullname):
    fio = fullname.strip().split(' ')
    p = Petrovich()
    fio[0] = p.lastname(fio[0], Case.GENITIVE)
    fio[1] = p.firstname(fio[1], Case.GENITIVE)
    fio[2] = p.lastname(fio[2], Case.GENITIVE)
    return ' '.join(fio)

@frappe.whitelist()
def director(fullname):
    fio = fullname.strip().split(' ')
    if fio[0].lower == 'председатель':
        fio[0] = 'Председателя'
    else:
        p = Petrovich()
        fio[0] = p.lastname(fio[0], Case.GENITIVE, Gender.MALE)
        if len(fio)>1:
            fio[1] = p.firstname(fio[1], Case.GENITIVE, Gender.MALE)
    return ' '.join(fio)
