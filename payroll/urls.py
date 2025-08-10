from django.urls import path
from .views import GeneratePayrollView, PayrollReportView

urlpatterns = [
    path('generate/', GeneratePayrollView.as_view(),name='payroll-generate'),
    path('report/', PayrollReportView.as_view()),
]
