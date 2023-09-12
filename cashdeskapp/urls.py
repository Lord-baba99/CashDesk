from django.urls import path
from . views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', cashdesk_home, name='cashdesk-home'),
    path('add-cashdesk-form', login_required(add_cashdesk_form), name='add-cashdesk-form'),
    path('cashdesk-config', login_required(cashdesk_config), name='cashdesk-config'),
    path('add-cashdesk', login_required(add_cashdesk), name='add-cashdesk'),
    path('cashdesk-operation-views/', login_required(cashdesk_operation_views), name='cashdesk-operation-views'),
    path('add-cashdesk-operation/', login_required(add_cashdesk_operation), name='add-cashdesk-operation'),
    path('delete-cashdesk-operation/<int:exercise>/<int:month>/<int:pk>', login_required(delete_cashdesk_operation), name='delete-cashdesk-operation'),
    path('update-cashdesk-operation/', login_required(update_cashdesk_operation), name='update-cashdesk-operation'),
    path('return-cashdesk-row/<int:exercise>/<int:month>/<int:pk>', login_required(return_cashdesk_row), name='return-cashdesk-row'),
    path('get-cashdesk-operation/<int:exercise>/<int:month>/<int:pk>', login_required(get_cashdesk_operation), name='get-cashdesk-operation'),
    path('search-cashdesk-operation/<int:exercise>/<int:month>', login_required(search_cashdesk_operation), name='search-cashdesk-operation'),
    path('add-continue-cashdesk-operation/', login_required(add_continue_cashdesk_operation), name="add-continue-cashdesk-operation"),
    path('cashdesk-operation-detail/<int:pk>', login_required(cashdesk_operation_detail), name="cashdesk-operation-detail"),
]
