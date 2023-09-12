from django.urls import path
from . views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	path('', bank_home, name='bank-home'),
	path('add-bank-form', login_required(add_bank_form), name='add-bank-form'),
	path('bank-account-config', login_required(bank_account_config), name='bank-account-config'),
	path('add-bank-account', login_required(add_bank_account), name='add-bank-account'),
	path('bank-operation-views/', login_required(bank_operation_views), name='bank-operation-views'),
	path('add-bank-operation/', login_required(add_bank_operation), name='add-bank-operation'),
	path('delete-bank-operation/<int:exercise>/<int:month>/<int:pk>', login_required(delete_bank_operation), name='delete-bank-operation'),
	path('update-bank-operation/', login_required(update_bank_operation), name='update-bank-operation'),
	path('return-bank-row/<int:exercise>/<int:month>/<int:pk>', login_required(return_bank_row), name='return-bank-row'),
	path('get-bank-operation/<int:exercise>/<int:month>/<int:pk>', login_required(get_bank_operation), name='get-bank-operation'),
	path('search-bank-operation/<int:exercise>/<int:month>', login_required(search_bank_operation), name='search-bank-operation'),
    path('add-continue-bank-operation/', login_required(add_continue_bank_operation), name="add-continue-bank-operation"),
    path('bank-operation-detail/<int:pk>', login_required(bank_operation_detail), name="bank-operation-detail"),
]