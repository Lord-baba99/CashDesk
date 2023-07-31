from django.urls import path
from . views import *

urlpatterns = [
    path('', cashdesk_home, name='cashdesk-home'),
    path('add-cashdesk-form', add_cashdesk_form, name='add-cashdesk-form'),
    path('cashdesk-config', cashdesk_config, name='cashdesk-config'),
    path('add-cashdesk', add_cashdesk, name='add-cashdesk'),
    path('cashdesk-operation-views/', cashdesk_operation_views, name='cashdesk-operation-views'),
    path('add-cashdesk-operation/', add_cashdesk_operation, name='add-cashdesk-operation'),
    path('delete-cashdesk-operation/<int:exercise>/<int:month>/<int:pk>', delete_cashdesk_operation, name='delete-cashdesk-operation'),
    path('update-cashdesk-operation/', update_cashdesk_operation, name='update-cashdesk-operation'),
    path('return-cashdesk-row/<int:exercise>/<int:month>/<int:pk>', return_cashdesk_row, name='return-cashdesk-row'),
    path('get-cashdesk-operation/<int:exercise>/<int:month>/<int:pk>', get_cashdesk_operation, name='get-cashdesk-operation'),
    path('search-cashdesk-operation/<int:exercise>/<int:month>', search_cashdesk_operation, name='search-cashdesk-operation'),
    path('add-continue-cashdesk-operation/', add_continue_cashdesk_operation, name="add-continue-cashdesk-operation"),
    path('cashdesk-operation-detail/<int:pk>', cashdesk_operation_detail, name="cashdesk-operation-detail"),
]
