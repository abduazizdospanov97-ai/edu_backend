from django.urls import path
from .views import DebtorListView

urlpatterns = [
    path('', DebtorListView.as_view(), name='debtors-list'),
    path('notify/', DebtorListView.as_view(), name='debtors-notify'),
]
