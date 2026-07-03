from django.urls import path, include

from rest_framework import routers

from softdesk.views import ProjectView



from authentication.viewsets import UserViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet)
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/project/', ProjectView.as_view()),
]
