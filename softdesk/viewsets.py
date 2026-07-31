from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated
from softdesk.permisssions import IsProjectAuthor, IsAdminAuthenticated
from softdesk.models import Project, Issue, Comment, Contributor
from softdesk.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer


class ProjectViewSet(ModelViewSet):
    
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminAuthenticated | IsProjectAuthor]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAdminAuthenticated | IsProjectAuthor]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Issue.objects.all()
        else:
            queryset = Issue.objects.filter(project__contributors__user=self.request.user)

        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminAuthenticated | IsProjectAuthor]

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.queryset = Comment.objects.all()
        else:
            self.queryset = Comment.objects.filter(issue__project__contributors__user=self.request.user)

        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            self.queryset = self.queryset.filter(issue_id=issue_id)

        return self.queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ContributorViewSet(ModelViewSet):

    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAdminAuthenticated | IsProjectAuthor]

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.queryset = Contributor.objects.all()
        else:
            self.queryset = Contributor.objects.filter(project__contributors__user=self.request.user)

        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            self.queryset = self.queryset.filter(project_id=project_id)

        return self.queryset