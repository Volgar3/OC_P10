from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):
    """Restrict write access on a `User` object to its own account.

    Any authenticated user can read another user's profile, but only
    the account owner can update or delete it.
    """

    def has_object_permission(self, request, view, obj):
        """Allow read access to anyone, write access to the owner only."""
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
