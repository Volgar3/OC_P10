from rest_framework.serializers import ModelSerializer 

from softdesk.models import Project

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('name','description','type','author','created_time') 