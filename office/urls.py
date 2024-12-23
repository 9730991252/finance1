from django.urls import path
from . import views

urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('employee/', views.employee, name='employee'),
    path('account_holder/', views.account_holder, name='account_holder'),
    path('collection/', views.collection, name='collection'),
    path('account_holder_details_collection/<int:id>', views.account_holder_details_collection, name='account_holder_details_collection'),
    path('account_type/', views.account_type, name='account_type'),
    path('add_account/<int:account_holder_id>', views.add_account, name='add_account'),
    path('daly_pdf/', views.daly_pdf, name='daly_pdf')
]
