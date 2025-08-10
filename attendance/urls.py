from django.urls import path
from .views import AttendanceCreateView, AttendanceListView

urlpatterns = [
    path('mark/', AttendanceCreateView.as_view(), name='mark-attendance'),
    path('logs/', AttendanceListView.as_view(), name='attendance-logs'),
]
