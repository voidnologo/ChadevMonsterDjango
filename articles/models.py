from django.db import models
from django_fsm import FSMField, transition


class Article(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    state = FSMField(default='submitted')

    def __str__(self):
        return self.title

    @transition(field=state, source='submitted', target='approved')
    def approve(self):
        pass

    @transition(field=state, source='approved', target='published')
    def publish(self):
        pass
