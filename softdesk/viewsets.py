from rest_framework.viewsets import ReadOnlyModelViewSet

from softdesk.models import Project, Issue, Comment
from softdesk.serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewSet(ReadOnlyModelViewSet):
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
    
    
class IssueViewSet(ReadOnlyModelViewSet):

    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset
    
class CommentViewSet(ReadOnlyModelViewSet):
    
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        self.queryset = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            self.queryset = self.queryset.filter(issue_id=issue_id)
            
        return self.queryset