from rest_framework.permissions import BasePermission

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','PUT','PATCH','DELETE']:
            return request.user.is_authenticated and request.user.role == 'recruiter'
        return True 
    
    def has_object_permission(self, request, view, obj):
        return obj.company == request.user 