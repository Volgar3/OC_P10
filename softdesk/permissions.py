from rest_framework.permissions import BasePermission, SAFE_METHODS
from softdesk.models import Comment, Contributor, Issue, Project


class IsAdminAuthenticated(BasePermission):
    """Grant access to authenticated superusers only.

    Intended to be combined with other permissions via the `|` operator@f
    so that admins can bypass business-rule checks (e.g. project
    membership) for supervision and development purposes.
    """

    def has_permission(self, request, view):
        """Return True if the requesting user is an authenticated superuser."""
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class IsProjectMember(BasePermission):
    """Restrict access to a project's resources based on contributor.

    Applies to `Project`, `Issue`, `Comment` and `Contributor` objects.
    Read access (`SAFE_METHODS`) is granted to any contributor of the
    related project; write access is granted to the project's author only.
    """

    def _get_project(self, obj):

        lambda_by_model = (
            (Project, lambda o: o),
            (Issue, lambda o: o.project),
            (Comment, lambda o: o.issue.project),
            (Contributor, lambda o: o.project),
        )

        for model_class, resolving_lambda in lambda_by_model:
            if isinstance(obj, model_class):
                return resolving_lambda(obj)

    def has_object_permission(self, request, view, obj):
        """Allow contributors to read; only the resource's own author writes.

        For `Issue`/`Comment`, the author to check is the object's own
        author, not the project's — a project owner does not automatically
        get edit/delete rights on someone else's issue or comment.
        """
        project = self._get_project(obj)
        is_contributor = bool(
            Contributor.objects.filter(project=project.id, user=request.user)
        )

        if request.method in SAFE_METHODS:
            return is_contributor

        if isinstance(obj, (Issue, Comment)):
            return request.user == obj.author

        return request.user == project.author

    def has_permission(self, request, view):
        """Making sure than user can create/edit/delete
        issues and comments in their own projects
        """
        if view.action != "create":
            return True

        issue_id = request.data.get("issue")
        project_id = request.data.get("project")
        if issue_id is not None:
            project_id = (
                Issue.objects.filter(id=issue_id)
                .values_list("project_id", flat=True)
                .first()
            )

        if project_id is None:
            return True

        # Only Author can add contributors
        if view.get_serializer_class().Meta.model is Contributor:
            is_author = bool(Project.objects.filter(id=project_id, author=request.user))
            return is_author
        # Make sur than Contributors can edit only their own project
        is_contributor = bool(
            Contributor.objects.filter(project=project_id, user=request.user)
        )
        return is_contributor
