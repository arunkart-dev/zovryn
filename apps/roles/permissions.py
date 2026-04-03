from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Only admin can create/update/delete records."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAnalystOrAdmin(BasePermission):
    """Analyst + Admin — used for dashboard access."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['analyst', 'admin']


class IsViewerOrAbove(BasePermission):
    """Viewer + Analyst + Admin — used for reading records."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['viewer', 'analyst', 'admin']