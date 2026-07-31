from django.urls import path, include

from rest_framework import routers

from softdesk.viewsets import ProjectViewSet, IssueViewSet, CommentViewSet

#Le routeur fait pour nous .as_view() lorsqu'il génère les urls
router = routers.SimpleRouter()
router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')
# router.register('contributor',ContributorViewSet, basename='contributor')
urlpatterns = [
    path('api/', include(router.urls)),
]
