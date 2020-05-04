from django.contrib.auth.models import User
from django.test import TestCase

from .models import Article


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
        url= 'http://example.org'
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
        self.assertEqual(article.url, 'http://example.org')
        self.assertEqual(article.state, 'submitted')
