from django.http import *
from django.shortcuts import *
from django.template.loader import *
from django.db.models import Q
from office.models import *

def search_account_holder(request):
    if request.method == 'GET':
        a = ''
        words = request.GET['words']
        if words:
            a = Account_holder.objects.filter(Q(holder_name__icontains=words) | Q(account_number__icontains=words),status=1).order_by('account_number')
    cotext={'a':a}
    t = render_to_string('ajax/search_account_holder.html', cotext)
    return JsonResponse({'t':t})

def save_holder_acount_type(request):
    if request.method == 'GET':
        account_holder_id = request.GET['account_holder_id']
        account_type_id = request.GET['account_type_id']
        print(account_holder_id, account_type_id)
        account = Account.objects.filter(account_holder_id=account_holder_id, account_type_id=account_type_id).first()
        if account:
            if account.status == 1:
                account.status = 0
                account.save()
            else:
                account.status = 1
                account.save()
        else:
            Account(
                account_holder_id=account_holder_id,
                account_type_id=account_type_id,
            ).save()
        return JsonResponse({'status':'success'})