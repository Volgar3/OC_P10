from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated
from softdesk.models import Project, Issue, Comment, Contributor
from softdesk.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer


class ProjectViewSet(ModelViewSet):
    
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()
    
    
class IssueViewSet(ModelViewSet):

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset
    
class CommentViewSet(ModelViewSet):
    
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = Comment.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            self.queryset = self.queryset.filter(issue_id=issue_id)
            
        return self.queryset
    
class ContributorViewSet(ModelViewSet):
    
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = Contributor.objects.all()
        contributor_id = self.request.GET.get('contributor_id')
        if contributor_id is not None:
            self.queryset = self.get_queryset(contributor_id=contributor_id)
        
        return self.queryset