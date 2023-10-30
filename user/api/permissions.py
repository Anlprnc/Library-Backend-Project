from rest_framework import permissions


class MemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'member'
    
    
class EmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'
    

class IsMemberOrEmployeeOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == 'member' or request.user.role == 'employee' or request.user.role == 'admin')
    
    
class IsEmployeeOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.role == 'employee' or request.user.role == 'admin')
    

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'