from django.shortcuts import render
from django.shortcuts import render, redirect
from office.models import *
from django.contrib import messages
import time
from datetime import date
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def account_type_daly_collection_pdf(request, id):
        account_holder = []
        a = Account_holder.objects.filter(status=1)
        for a in a:
            t = Transition.objects.filter(account_holder_id=a.id,date=date.today()).last()
            if t != None:
                amount = Transition.objects.filter(account_holder_id=a.id,account__account_type_id=id, date=date.today()).aggregate(Sum('credit_amount'))
                account_holder.append({'amount':amount['credit_amount__sum'], 'id':a.id,'account_number':a.account_number,'holder_name':a.holder_name,'date':t.added_date})
        context={
            'account_holder':account_holder,
            'account_type':Account_type.objects.filter(id=id).first()
        }
        return render(request, 'pdf/account_type_daly_collection_pdf.html', context)