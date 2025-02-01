from django.urls import path
from . import views

urlpatterns = [
    path('account_type_daly_collection_pdf/<int:id>', views.account_type_daly_collection_pdf, name='account_type_daly_collection_pdf'),
    path('all_report_pdf/<str:from_date>/<str:to_date>', views.all_report_pdf, name=' all_report_pdf')
]
