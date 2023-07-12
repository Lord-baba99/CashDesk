from django.urls import path
from . views import bank_home

urlpatterns = [
	path('', bank_home, name='bank-home'),
	path('add-bank-operation/', add_bank_operation, name='add-bank-operation'),
    path('add-continue-bank-operation/', add_continue_bank_operation, name="add-continue-bank-operation"),
    path('bank-operation-detail/<str:pk>', bank_operation_detail, name="bank-operation-detail"),
    path('bank-operation/', bank, name='bank-operation'),
]