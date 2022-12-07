from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        
        return obj == request.user or request.user.is_staff