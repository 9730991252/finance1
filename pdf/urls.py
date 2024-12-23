from django.urls import path
from . import views

urlpatterns = [
    path('account_type_daly_collection_pdf/<int:id>', views.account_type_daly_collection_pdf, name='account_type_daly_collection_pdf'),

]
