from django.conf.urls import url, include
from rest_framework import routers
from .views import LockViewSet

router = routers.DefaultRouter()
router.register(r'locks', LockViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]