from rest_framework import permissions
from .models import User


class MyPermission(permissions.BasePermission):

    def __init__(self, allowed_methods):
        super().__init__()
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return request.method in self.allowed_methods and request.user.is_company_admin
