from django.urls import path
from .views import DashboardStatsView, DashboardRevenueView, DashboardRecentPaymentsView

urlpatterns = [
    path('stats/',           DashboardStatsView.as_view(),          name='dashboard-stats'),
    path('revenue/',         DashboardRevenueView.as_view(),         name='dashboard-revenue'),
    path('recent-payments/', DashboardRecentPaymentsView.as_view(),  name='dashboard-recent-payments'),
]
