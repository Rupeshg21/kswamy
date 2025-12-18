from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DonorViewSet, 
    ExpenseViewSet, 
    RenovationGoalViewSet,
    DashboardView,
    RecentActivityView,
    ChartsDataView
)

router = DefaultRouter()
router.register(r'donors', DonorViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'renovation-goals', RenovationGoalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('recent-activity/', RecentActivityView.as_view(), name='recent-activity'),
    path('charts-data/', ChartsDataView.as_view(), name='charts-data'),
]