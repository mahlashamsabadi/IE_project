from rest_framework.permissions import BasePermission 
class IsDhcpManager(BasePermission):
    message = 'permission denied, you are not Dhcp manager'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user
    
    def has_object_permission(self, request, view, obj):
        return request.user.type == "dhcp"


class IsMailManager(BasePermission):
    message = 'permission denied, you are not mail manager'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user
    
    def has_object_permission(self, request, view, obj):
        return request.user.type == "mail"
class IsWebManager(BasePermission):
    message = 'permission denied, you are not web manager'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user
    
    def has_object_permission(self, request, view, obj):
        return request.user.type == "web"
