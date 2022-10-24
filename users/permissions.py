from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import permissions

from .models import User


class LoginPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.user.is_superuser:
            return True

        return False


class GeneralPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.user.is_superuser:
            return True

        serializer = get_object_or_404(User, pk=view.kwargs.get('pk'))

        return (
            request.user.is_authenticated
            and request.user.id == serializer.id
        )


class ListCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.user.is_superuser:
            return True

        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )
