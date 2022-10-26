from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'projects', views.ProjectsViewSet)
router.register(r'targets', views.TargetsViewSet)
router.register(r'scans', views.ScansViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
