from django_fsm import can_proceed
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from . import serializers


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        return self.transition_to('approve')

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        return self.transition_to('reject')

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        return self.transition_to('publish')

    def transition_to(self, next_state):
        article = self.get_object()
        transition = getattr(article, next_state)
        if not can_proceed(transition):
            return Response({'status': 'invalid state change'})
        transition()
        article.save()
        return Response({'status': article.state})
