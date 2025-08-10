from rest_framework import generics, permissions
from .models import Attendance
from .serializers import AttendanceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from datetime import datetime

class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Attendance.objects.all()
        employee_id = self.request.query_params.get('user')
        date = self.request.query_params.get('date')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        if employee_id:
            queryset = queryset.filter(user_id=employee_id)

        if date:
            date_obj = datetime.strptime(date.strip(), "%Y-%m-%d")
            queryset = queryset.filter(timestamp__date=date_obj)

        if month and year:
            queryset = queryset.filter(timestamp__month=month, timestamp__year=year)

        return queryset.order_by('-timestamp')
