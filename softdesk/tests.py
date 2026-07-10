from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from softdesk.models import Project, Issue, Comment, Contributor
from authentication.models import User


class TestProject(APITestCase):
    
    url = reverse_lazy('project-list')

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        project_1 = Project.objects.create(name='P1', type='back-end')
        project_2 = Project.objects.create(name='P2', type='iOS')

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                'name': project_1.name,
                'description': project_1.description,
                'type': project_1.type,
                'author': project_1.author,
                'created_time': self.format_datetime(project_1.created_time),
            },
            {
                'name': project_2.name,
                'description': project_2.description,
                'type': project_2.type,
                'author': project_2.author,
                'created_time': self.format_datetime(project_2.created_time),
            },
        ]

        self.assertEqual(expected, response.json())


class Testissue(APITestCase):
    
    url = reverse_lazy ('issue-list')
    
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        hugo = User.objects.create_user(username='Hugo', password='test1234', age=25)
        aurelien = User.objects.create_user(username='Aurelien', password='test1234', age=30)
        project_1 = Project.objects.create(name='P1', type='back-end')
        project_2 = Project.objects.create(name='P2', type='iOS')
        issue_1 = Issue.objects.create(name='Issue 1', priority='LOW', tag='BUG', status='In Progress', author=hugo, project=project_1)
        issue_2 = Issue.objects.create(name='Issue_2', priority='MEDIUM', tag='FEATURE', status='To Do', author=aurelien, project=project_2)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        expected = [
            {
                'name': issue_1.name,
                'description': issue_1.description,
                'tag': issue_1.tag,
                'priority': issue_1.priority,
                'status': issue_1.status,
                'author': issue_1.author.username,
                'assignee': issue_1.assignee,
                'project': issue_1.project.name,
            },
            {
                'name': issue_2.name,
                'description': issue_2.description,
                'tag': issue_2.tag,
                'priority': issue_2.priority,
                'status': issue_2.status,
                'author': issue_2.author.username,
                'assignee': issue_2.assignee,
                'project': issue_2.project.name,

            }
        ]
        self.assertEqual(expected, response.json())
