import django_fsm
from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article


class ArticleTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_403_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 403)

    def test_get_request_for_articles_returns_all_articles(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        a2 = Article.objects.create(title='Test2', url='example.org')
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)
        expected = [
            {'title': 'Test1', 'url': 'example.com', 'id': 1, 'state': 'submitted'},
            {'title': 'Test2', 'url': 'example.org', 'id': 2, 'state': 'submitted'}
        ]
        self.assertEqual(response.json(), expected)

    def test_post_creates_an_article(self):
        title = 'new article'
        url= 'http://localhost'
        data  = {
            'title': title,
            'url': url,
        }
        response = self.client.post('/api/articles/', data=data)
        self.assertEqual(response.status_code, 201)
        articles = Article.objects.all()
        self.assertEqual(len(articles), 1)
        article = articles.get()
        self.assertEqual(article.title, title)
        self.assertEqual(article.url, url)
        self.assertEqual(article.state, 'submitted')

    def test_approve_an_article(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        response = self.client.post(f'/api/articles/{a1.pk}/approve/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'approved'})
        a = Article.objects.get(pk=a1.pk)
        self.assertEqual(a.state, 'approved')

    def test_reject_an_article(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        response = self.client.post(f'/api/articles/{a1.pk}/reject/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'rejected'})
        a = Article.objects.get(pk=a1.pk)
        self.assertEqual(a.state, 'rejected')

    def test_publish_an_article(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        a1.approve()
        a1.save()
        response = self.client.post(f'/api/articles/{a1.pk}/publish/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'published'})
        a = Article.objects.get(pk=a1.pk)
        self.assertEqual(a.state, 'published')

    def test_cannot_approve_an_article_if_it_is_rejected(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        a1.reject()
        a1.save()
        response = self.client.post(f'/api/articles/{a1.pk}/approve/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'invalid state change'})
        a = Article.objects.get(pk=a1.pk)
        self.assertEqual(a.state, 'rejected')

    def test_cannot_reject_an_article_if_it_is_approved(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        a1.approve()
        a1.save()
        response = self.client.post(f'/api/articles/{a1.pk}/reject/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'invalid state change'})
        a = Article.objects.get(pk=a1.pk)
        self.assertEqual(a.state, 'approved')

    def test_cannot_publish_an_article_if_it_is_rejected(self):
        a1 = Article.objects.create(title='Test1', url='example.com')
        a1.reject()
        a1.save()
        response = self.client.post(f'/api/articles/{a1.pk}/publish/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'invalid state change'})
        a = Article.objects.get(pk=a1.pk)
        self.assertEqual(a.state, 'rejected')
