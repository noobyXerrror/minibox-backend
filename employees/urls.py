# employees/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import EmployeeViewSet

router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),  # ✅ wrap router.urls in include()
]
