from rest_framework.serializers import ModelSerializer, StringRelatedField

from softdesk.models import Project, Issue, Comment

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('name','description','type','author','created_time') 
        
class IssueSerializer(ModelSerializer):
    project = StringRelatedField()
    author = StringRelatedField()
    tag = StringRelatedField()
    
    class Meta:
        model = Issue
        fields = ('name','priority','tag','description','status','project', 'author', 'assignee')
        
class CommentSerializer(ModelSerializer):
    description = StringRelatedField()
    issue = StringRelatedField()
    author = StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ('uuid','description','issue','author')
        
        