from rest_framework.viewsets import ReadOnlyModelViewSet

from softdesk.models import Project
from softdesk.serializers import ProjectSerializer


class ProjectViewSet(ReadOnlyModelViewSet):
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
        