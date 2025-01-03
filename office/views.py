from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import time
from datetime import date
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
        }
        return render(request, 'office/office_home.html', context)
    else:
        return redirect('login')
    
def daly_pdf(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        account_holder = []
        a = Account_holder.objects.filter(status=1)
        for a in a:
            t = Transition.objects.filter(account_holder_id=a.id,date=date.today()).first()
            if t != None:
                account_holder.append({'id':a.id,'account_number':a.account_number,'holder_name':a.holder_name,'date':t.added_date})
        context={
            'e':e,
            'account_holder':account_holder,
            'account_type':Account_type.objects.filter(status=1),
            'date':date.today(),
            'total': Transition.objects.filter(date=date.today()).aggregate(Sum('credit_amount'))['credit_amount__sum']
        }
        return render(request, 'office/daly_pdf.html', context)
    else:
        return redirect('login')
    
    
    
def add_account(request, account_holder_id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        if e:
            pass
        else:
            return redirect('login')
        context={
            'e':e,
            'account_holder':Account_holder.objects.filter(id=account_holder_id).first(),
            'account_type':Account_type.objects.all(),
        }
        return render(request, 'office/add_account.html', context)
    else:
        return redirect('login')
    
def account_type(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        if e:
            if 'Add_account_type'in request.POST:
                name = request.POST.get('name')
                Account_type(
                    name=name,
                ).save()
                return redirect('account_type')
            if 'Edit_account_type'in request.POST:
                id = request.POST.get('id')
                name = request.POST.get('name')
                a = Account_type.objects.filter(id=id).first()
                a.name = name
                a.save()
                return redirect('account_type')
            if 'active'in request.POST:
                id = request.POST.get('id')
                c = Account_type.objects.filter(id=id).first()
                c.status = 0
                c.save()
                return redirect('account_type')
            if 'deactive'in request.POST:
                id = request.POST.get('id')
                c = Account_type.objects.filter(id=id).first()
                c.status = 1
                c.save()
                return redirect('account_type')
        else:
            return redirect('login')
        context={
            'e':e,
            'account_type':Account_type.objects.all(),
        }
        return render(request, 'office/account_type.html', context)
    else:
        return redirect('login')
    

def account_holder_details_collection(request, id):
    if request.session.has_key('office_mobile'):
        momile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=momile).first()
        if e:
            account = Account.objects.filter(account_holder_id=id,status=1)
            if 'Collect_amount'in request.POST:
                for a in account:
                    name = f'{a.account_type.name}amount'
                    amount = request.POST.get(name)
                    if amount != 0:
                        Transition(
                            collected_by_id=e.id,
                            account_holder_id=id,
                            account_id=a.id,
                            credit_amount=amount,
                            remark = 'जमा'
                        ).save()
                    else:
                        messages.warning(request, f"please enter amount for {a.account_type.name}")
                        break
                return redirect(f'/office/account_holder_details_collection/{id}')
        else:
            return redirect('login')
        context={
            'e':e,
            'account_holder':Account_holder.objects.filter(id=id).first(),
            'last_five_transaction':Transition.objects.filter(account_holder_id=id).order_by('-id')[:5],
            'account':account,

        }
        return render(request, 'office/account_holder_details_collection.html', context)
    
def collection(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        context={
            'e':e,
        }
        return render(request, 'office/collection.html', context)
    else:
        return redirect('login')
    
def employee(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        if e:
            if 'Add_employee'in request.POST:
                name = request.POST.get('name')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                if Office_employee.objects.filter(mobile=mobile).exists():
                    messages.warning(request, f"Employee already exists with mobile number - {mobile}")
                else:
                    Office_employee(
                        added_by_id=e.id,
                        name=name,
                        mobile=mobile,
                        pin=pin,
                    ).save()
                return redirect('employee')
            if 'Edit_employee'in request.POST:
                id = request.POST.get('id')
                name = request.POST.get('name')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                o = Office_employee.objects.filter(id=id).first()
                if Office_employee.objects.filter(mobile=mobile).exclude(id=id).exists():
                    messages.warning(request, f"Employee already exists with mobile number - {mobile}")
                else:
                    o.name = name
                    o.mobile = mobile   
                    o.pin = pin
                    o.save()
                if o.id == e.id:
                    del request.session['office_mobile']
                    return redirect('login')
                return redirect('employee')
            if 'active'in request.POST:
                id = request.POST.get('id')
                c = Office_employee.objects.filter(id=id).first()
                c.status = 0
                c.save()
                return redirect('employee')
            if 'deactive'in request.POST:
                id = request.POST.get('id')
                c = Office_employee.objects.filter(id=id).first()
                c.status = 1
                c.save()
                return redirect('employee')
        else:
            return redirect('login')
        context={
            'e':e,
            'employee':Office_employee.objects.all(),
        }
        return render(request, 'office/employee.html', context)
    else:
        return redirect('login')

def account_holder(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = Office_employee.objects.filter(mobile=mobile).first()
        if e:
            if 'Add_account_holder'in request.POST:
                holder_name = request.POST.get('holder_name')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                account_number = request.POST.get('account_number')
                if Account_holder.objects.filter(mobile=mobile).exists():
                    messages.warning(request, f"खातेदार already exists with mobile number - {mobile}")
                else:
                    Account_holder(
                        holder_name=holder_name,
                        mobile=mobile,
                        pin=pin,
                        account_number=account_number,
                    ).save()
                return redirect('account_holder')
            if 'Edit_account_holder'in request.POST:
                id = request.POST.get('id')
                holder_name = request.POST.get('holder_name')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                account_number = request.POST.get('account_number')
                a = Account_holder.objects.filter(id=id).first()
                if Account_holder.objects.filter(mobile=mobile).exclude(id=id).exists():
                    messages.warning(request, f"खातेदार already exists with mobile number - {mobile}")
                else:
                    a.holder_name = holder_name
                    a.mobile = mobile   
                    a.pin = pin
                    a.account_number = account_number
                    a.save()
                return redirect('account_holder')
            if 'active'in request.POST:
                id = request.POST.get('id')
                c = Account_holder.objects.filter(id=id).first()
                c.status = 0
                c.save()
                return redirect('account_holder')
            if 'deactive'in request.POST:
                id = request.POST.get('id')
                c = Account_holder.objects.filter(id=id).first()
                c.status = 1
                c.save()
                return redirect('account_holder')
        else:
            return redirect('login')
        context={
            'e':e,
            'account_holder':Account_holder.objects.all().order_by('account_number'),
        }
        return render(request, 'office/account_holder.html', context)
    else:
        return redirect('login')