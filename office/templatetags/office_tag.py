from django import template
from office.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
from django.utils.safestring import mark_safe
register = template.Library()
@register.simple_tag()
def account_holder_available_balence(account_holder_id):
    credit = Transition.objects.filter(account_holder_id=account_holder_id).aggregate(Sum('credit_amount'))
    debit = Transition.objects.filter(account_holder_id=account_holder_id).aggregate(Sum('debit_amount'))
    if credit['credit_amount__sum'] is None:
        credit['credit_amount__sum'] = 0
    if debit['debit_amount__sum'] is None:
        debit['debit_amount__sum'] = 0
    total_avalable_balence = (credit['credit_amount__sum'] - debit['debit_amount__sum'])
    return total_avalable_balence


@register.inclusion_tag('inclusion_tag/office/todays_collection.html')
def todays_collection():
    todays_collection = Transition.objects.filter(date=date.today()).aggregate(Sum('credit_amount'))
    o = Office_employee.objects.filter(status=1)
    office_employee = []
    for i in o:
        a = Transition.objects.filter(date=date.today(), collected_by_id=i.id).aggregate(Sum('credit_amount'))
        a = a['credit_amount__sum']
        if a is None:
            a = 0
        office_employee.append({
            'id':i.id,
            'name': i.name,
            'credit_amount': a
        })
    return {
        'todays_collection': todays_collection['credit_amount__sum'],
        'office_employee': office_employee,
        'account_types':Account_type.objects.filter(status=1)
        }
    
@register.inclusion_tag('inclusion_tag/office/summary.html')
def summary():
    total_account_holder = Account_holder.objects.all().count()
    total_collection = Transition.objects.aggregate(Sum('credit_amount'))
    total_withdrawal = Transition.objects.aggregate(Sum('debit_amount'))
    total_office_employee = Office_employee.objects.filter(status=1).count()
    if total_collection['credit_amount__sum'] is None:
        total_collection['credit_amount__sum'] = 0
    if total_withdrawal['debit_amount__sum'] is None:
        total_withdrawal['debit_amount__sum'] = 0
    return {
        'total_account_holder': total_account_holder,
        'total_withdrawal': total_withdrawal['debit_amount__sum'],
        'total_office_employee': total_office_employee,
    }

@register.simple_tag() 
def check_account_holde_account(account_type_id, account_holder_id):
    if Account.objects.filter(status=1, account_holder_id=account_holder_id, account_type_id=account_type_id).exists():
        return 1
    else:
        return 0
    
@register.simple_tag() 
def account_type_daly_collection_total_amount(office_employee_id, account_type_id):
    print(office_employee_id)
    amount = Transition.objects.filter(date=date.today(), collected_by_id=office_employee_id,account__account_type_id=account_type_id).aggregate(Sum('credit_amount'))
    if amount['credit_amount__sum'] is None:
        return 0
    return amount['credit_amount__sum']

@register.simple_tag() 
def account_type_daly_collection_count(office_employee_id, account_type_id):
    total_count = Account.objects.filter(account_type_id=account_type_id, status=1).count()
    paid_count = Transition.objects.filter(date=date.today(), collected_by_id=office_employee_id,account__account_type_id=account_type_id).count()
    un_paid_count = (int(total_count) - int(paid_count))
    t = ('(<b class="text-success">'+ str(paid_count) +'</b> / <b class="text-danger">'+ str(un_paid_count) +'</b> = '+ str(total_count) +')')
    return mark_safe(t)

    
@register.inclusion_tag('inclusion_tag/office/account_holder_last_five_transaction.html')
def account_holder_last_five_transaction(account_id):
    last_five_transaction = Transition.objects.filter(account_id=account_id).order_by('-id')[:5]
    
    credit = Transition.objects.filter(account_id=account_id).aggregate(Sum('credit_amount'))
    debit = Transition.objects.filter(account_id=account_id).aggregate(Sum('debit_amount'))
    if credit['credit_amount__sum'] is None:
        credit['credit_amount__sum'] = 0
    if debit['debit_amount__sum'] is None:
        debit['debit_amount__sum'] = 0
    total_avalable_balence = (credit['credit_amount__sum'] - debit['debit_amount__sum'])
    
    return {
        'last_five_transaction': last_five_transaction,
        'total_avalable_balence': total_avalable_balence,
        'account_id':account_id
        }
    
@register.inclusion_tag('inclusion_tag/office/account_holder_daly_collection.html')
def account_holder_daly_collection(account_holder_id):
    account = []
    a = Account.objects.filter(account_holder_id=account_holder_id, status=1)
    total_amount = 0
    for a in a:
        am = Transition.objects.filter(date=date.today(), account_id=a.id).aggregate(Sum('credit_amount'))
        am = am['credit_amount__sum']
        if am:
            total_amount += am
            account.append({
                'name': a.account_type.name,
                'amount': am,
                'id':a.id
            })
    return{
        'account':account,
        'account_holder_id':account_holder_id,
        'count':Account.objects.filter(account_holder_id=account_holder_id,status=1).count(),
        'total_amount':total_amount
    }
    


@register.simple_tag()
def todays_account_transaction(account_id):
    tr = []
    for t in Transition.objects.filter(account_id=account_id,date=date.today()):
        tr.append({'amount':t.credit_amount})
    return tr

@register.simple_tag()
def account_total(account_holder_id, account_type_id):
    tr = Transition.objects.filter(account__account_type_id=account_type_id,account_holder_id=account_holder_id,date=date.today())
    t = tr.aggregate(Sum('credit_amount'))['credit_amount__sum']
    if t is None:
        total = '--'
    else:
        total = f'{t}'
    return total

@register.simple_tag()
def all_account_total(from_date, to_date ,account_holder_id, account_type_id):
    tr = Transition.objects.filter(account__account_type_id=account_type_id,account_holder_id=account_holder_id,date__gte=from_date,date__lte=to_date)
    t = tr.aggregate(Sum('credit_amount'))['credit_amount__sum']
    if t is None:
        total = '--'
    else:
        total = f'{t}'
    return total

@register.simple_tag()
def account_type_total(account_type_id):
    tr = Transition.objects.filter(account__account_type_id=account_type_id,date=date.today())
    t = tr.aggregate(Sum('credit_amount'))['credit_amount__sum']
    if t is None:
        total = '--'
    else:
        total = f'{t}'
    return total

@register.simple_tag()
def account_type_total_report(from_date, to_date ,account_type_id):
    tr = Transition.objects.filter(account__account_type_id=account_type_id,date__gte=from_date,date__lte=to_date)
    t = tr.aggregate(Sum('credit_amount'))['credit_amount__sum']
    if t is None:
        total = '--'
    else:
        total = f'{t}'
    return total