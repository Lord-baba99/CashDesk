from django.urls import path
from . views import *

urlpatterns = [
	path('', bank_home, name='bank-home'),
	path('add-bank-form', add_bank_form, name='add-bank-form'),
	path('bank-account-config', bank_account_config, name='bank-account-config'),
	path('add-bank-account', add_bank_account, name='add-bank-account'),
	path('bank-operation-views/', bank_operation_views, name='bank-operation-views'),
	path('add-bank-operation/', add_bank_operation, name='add-bank-operation'),
	path('delete-bank-operation/<int:exercise>/<int:month>/<int:pk>', delete_bank_operation, name='delete-bank-operation'),
	path('update-bank-operation/', update_bank_operation, name='update-bank-operation'),
	path('return-bank-row/<int:exercise>/<int:month>/<int:pk>', return_bank_row, name='return-bank-row'),
	path('get-bank-operation/<int:exercise>/<int:month>/<int:pk>', get_bank_operation, name='get-bank-operation'),
	path('search-bank-operation/<int:exercise>/<int:month>', search_bank_operation, name='search-bank-operation'),
    path('add-continue-bank-operation/', add_continue_bank_operation, name="add-continue-bank-operation"),
    path('bank-operation-detail/<int:pk>', bank_operation_detail, name="bank-operation-detail"),
]