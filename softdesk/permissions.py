from rest_framework.permissions import BasePermission, SAFE_METHODS
from softdesk.models import Comment, Contributor, Issue, Project


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_superuser)


class IsProjectMember(BasePermission):
    def _get_project(self, obj):
        lambda_by_model = (
            (Project, lambda o: o),
            (Issue, lambda o: o.project),
            (Comment, lambda o: o.issue.project)
        )

        for model_class, resolving_lambda in lambda_by_model:
            if isinstance(obj, model_class):
                return resolving_lambda(obj)

    def has_object_permission(self, request, view, obj):
        print(obj)
        project = self._get_project(obj)
        is_author = request.user == project.author
        is_contributor = bool(Contributor.objects.filter(project=project.id, user=request.user))

        if request.method in SAFE_METHODS:
            return is_contributor

        return is_author

