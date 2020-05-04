from django.db import models
from django_fsm import FSMField, transition, RETURN_VALUE


class Article(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    state = FSMField(default='submitted', protected=True)

    def __str__(self):
        return self.title

    @transition(field=state, source='submitted', target=RETURN_VALUE('approved', 'rejected'))
    def approve(self, approve=True):
        return 'approved' if approve else 'rejected'

    @transition(field=state, source='approved', target='published')
    def publish(self):
        pass
