from rest_framework.permissions import BasePermission,SAFE_METHODS
from app.models import Review
class ReviewPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if Review.objects.filter(user=request.user).exists():
                return False
            else:
                return True
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.user == obj.user:
                return True
            else:
                return False
class OrderPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if request.user.is_staff or request.user.is_superuser:
                return True
            else:
                return False