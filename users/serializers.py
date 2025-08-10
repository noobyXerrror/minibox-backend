from rest_framework import serializers
from employees.models import Employee
from attendance.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['status', 'timestamp']

class EmployeeWithAttendanceSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'department', 'monthly_salary', 'attendance']

    def get_attendance(self, obj):
        attendances = Attendance.objects.filter(user=obj.user).order_by('-timestamp')
        return AttendanceSerializer(attendances, many=True).data
