from rest_framework import permissions


class MemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'member'
    
    
class EmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'