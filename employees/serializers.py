from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Employee

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['user']

    def get_user_name(self, obj):
        return obj.user.name if obj.user else None

    def create(self, validated_data):
        # Extract the email
        user_email = validated_data.pop('user_email', None)

        try:
            # Only allow users who are NOT employees yet
            user = User.objects.get(email=user_email)
            if Employee.objects.filter(user=user).exists():
                raise serializers.ValidationError({"user_email": "This user is already an employee."})
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_email": "No user with this email found."})

        validated_data['user'] = user
        return super().create(validated_data)
