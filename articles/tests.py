from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Article, Publisher


class ArticleTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.editor = User.objects.create_user(
            username="editor", password="pass", role="editor"
        )
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=self.editor,
            publisher=self.publisher,
        )

    def test_article_approval(self):
        self.article.approved = True
        self.article.save()
        self.assertTrue(self.article.approved)
