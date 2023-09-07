from django.urls import path

from . import views

#app_name = 'borrow'

urlpatterns = [
    path('resources/<int:resource_id>/borrow/', views.borrow_resource, name='borrow-resource'),
    path('transactions/<int:transaction_id>/extend/', views.extend_due_date, name='extend-due-date'),
    path('transactions/<int:transaction_id>/return/', views.return_resource, name='return-resource'),
    path('transactions/current/', views.get_actual_borrowed_resources, name='get-current-borrowed-resources'),
    path('transactions/previous/', views.get_previous_borrowed_resources, name='get-previous-borrowed-resources'),
]
