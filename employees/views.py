from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsHRorSelf

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsHRorSelf]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # HR
            return Employee.objects.all()
        return Employee.objects.filter(user=user)  # Employee → only self

    def perform_create(self, serializer):
        # No change here — HR provides the email, serializer sets user automatically
        serializer.save()
