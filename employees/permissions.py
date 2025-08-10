from rest_framework.permissions import BasePermission

class IsHRorSelf(BasePermission):
    """
    HR (is_staff=True) can access all employees.
    Regular employees can only access their own profile.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True  # HR can access everything
        return obj.user == request.user  # Employee can only access self
