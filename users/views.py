from django.shortcuts import render
from employees.models import Employee
from users.permissions import IsAdmin, IsEmployee, IsHR
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
User = get_user_model()

# users/views.py
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if not raw_token:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
    
class AuthStatusView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"authenticated": True})

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "EMPLOYEE")  # Defaults to EMPLOYEE
        name = request.data.get("name", "")

        if not email or not password:
            return Response({"error": "Username and password are required"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            name=name
        )
        return Response({"message": f"{role} user created successfully."}, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({"message": "Login successful", "role": user.role}, status=200)

        # Set cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax',
        )

        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=205)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


@api_view(["POST"])
def refresh_token_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token is None:
        return Response({"error": "Refresh token not provided"}, status=400)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response({"message": "Token refreshed"}, status=200)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
        )
        return response
    except Exception as e:
        return Response({"error": "Invalid refresh token"}, status=400)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": f"Welcome to the Admin dashboard, {request.user.name}!"})


from .serializers import EmployeeWithAttendanceSerializer

class HRDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'HR':
            return Response({"error": "Unauthorized"}, status=403)

        users = User.objects.select_related('user').all()

        data = [
            {
               "email":user.email
            }
            for user in users
        ]
        return Response({"employees": data})

class EmployeeDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsEmployee]

    def get(self, request):
        return Response({"message": f"Welcome to the Employee dashboard, {request.user.name}!"})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_users_for_employee(request):
    """
    Returns all users who are not yet linked to an Employee.
    Intended for HR dropdown when adding new employees.
    """
    if request.user.role != 'HR':
        return Response({"error": "Unauthorized"}, status=403)

    # Get IDs of users who are already employees
    employee_user_ids = Employee.objects.values_list('user_id', flat=True)

    # Filter users who are NOT in the employee list
    available_users = User.objects.exclude(id__in=employee_user_ids)

    data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in available_users
    ]
    return Response(data)