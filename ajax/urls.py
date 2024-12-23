from django.urls import path
from . import views

urlpatterns = [
    path('search_account_holder/', views.search_account_holder, name='search_account_holder'),
    path('save_holder_acount_type/', views.save_holder_acount_type, name='save_holder_acount_type'),
]