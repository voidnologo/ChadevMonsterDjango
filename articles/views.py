from rest_framework import permissions, viewsets

from . import models
from . import serializers


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
