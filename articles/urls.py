from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'articles', views.ArticlesViewSet)


app_name = 'articles'
urlpatterns = [
    path('', include(router.urls)),
]
