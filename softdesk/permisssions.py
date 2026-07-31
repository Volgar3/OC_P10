from rest_framework.permissions import BasePermission, SAFE_METHODS
from softdesk.models import Contributor


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_superuser)


class IsProjectAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        author = obj.project.author if isinstance(obj, Contributor) else obj.author
        return author == request.user

