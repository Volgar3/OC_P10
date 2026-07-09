from django.urls import path, include

from rest_framework import routers

from softdesk.viewsets import ProjectViewSet

from authentication.viewsets import UserViewSet

#Le routeur fait pour nous .as_view() lorsqu'il génère les urls
router = routers.SimpleRouter()
router.register('project', ProjectViewSet, basename='project')


router.register(r"users", UserViewSet)
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
