from rest_framework.serializers import ModelSerializer, StringRelatedField

from softdesk.models import Project, Issue, Comment, Contributor

class ProjectSerializer(ModelSerializer):
    author = StringRelatedField()
    contributors = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id','name','description','type','author','created_time','contributors')
        read_only_fields = ('author',)
        
class IssueSerializer(ModelSerializer):
    author = StringRelatedField()

    class Meta:
        model = Issue
        fields = ('id','name','priority','tag','description','status','project', 'author', 'assignee')
        read_only_fields = ('author',)

class CommentSerializer(ModelSerializer):
    author = StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id','uuid','description','issue','author')
        read_only_fields = ('author',)
        
class ContributorSerializer(ModelSerializer):
    project = StringRelatedField()
    user = StringRelatedField()
    
    class Meta:
        model = Contributor
        fields = ('id','user','project')