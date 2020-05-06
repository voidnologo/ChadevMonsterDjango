import django_fsm
from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article


class ArticleTests(TestCase):

    def test_approve(self):
        article = Article.objects.create(title='test', url='example.org')
        self.assertEqual(article.state, 'submitted')
        article.approve()
        self.assertEqual(article.state, 'approved')

    def test_reject(self):
        article = Article.objects.create(title='test', url='example.org')
        self.assertEqual(article.state, 'submitted')
        article.reject()
        self.assertEqual(article.state, 'rejected')

    def test_cannot_be_published_if_in_submit_state(self):
        article = Article.objects.create(title='test', url='example.org')
        self.assertEqual(article.state, 'submitted')
        with self.assertRaises(django_fsm.TransitionNotAllowed) as exc:
            article.publish()
        self.assertEqual(str(exc.exception), "Can't switch from state 'submitted' using method 'publish'")

    def test_cannot_be_published_if_in_rejected_state(self):
        article = Article.objects.create(title='test', url='example.org')
        article.reject()
        self.assertEqual(article.state, 'rejected')
        with self.assertRaises(django_fsm.TransitionNotAllowed) as exc:
            article.publish()
        self.assertEqual(str(exc.exception), "Can't switch from state 'rejected' using method 'publish'")

    def test_publish(self):
        article = Article.objects.create(title='test', url='example.org')
        article.approve()
        self.assertEqual(article.state, 'approved')
        article.publish()
        self.assertEqual(article.state, 'published')
