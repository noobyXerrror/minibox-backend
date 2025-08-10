
from django.urls import path
from .views import AdminDashboardView, AuthStatusView, EmployeeDashboardView, HRDashboardView, SignupView, LoginView, LogoutView, available_users_for_employee, refresh_token_view

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
       path('refresh/', refresh_token_view, name='token_refresh'),
    path('status/', AuthStatusView.as_view(), name='auth-status'),
    path('available-users/', available_users_for_employee, name='available_users'),
 # Dashboards
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/hr/', HRDashboardView.as_view(), name='hr_dashboard'),
    path('dashboard/employee/', EmployeeDashboardView.as_view(), name='employee_dashboard'),
]
