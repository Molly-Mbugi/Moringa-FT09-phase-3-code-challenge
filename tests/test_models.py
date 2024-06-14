import unittest
import sqlite3
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.connection import get_db_connection
from database.setup import create_tables

class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_tables()  
        cls.conn = get_db_connection()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        # Clear tables before each test
        with self.conn:
            self.conn.execute("DELETE FROM authors")
            self.conn.execute("DELETE FROM articles")
            self.conn.execute("DELETE FROM magazines")

    def test_author_creation(self):
        author = Author(name="John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        author = Author(name="John Doe")
        author.save()
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        article = Article(title="Test Title", content="Test Content", author_id=author.id, magazine_id=magazine.id)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_save_and_fetch(self):
        author = Author(name="John Doe")
        author.save()
        saved_author = Author.get_by_id(author.id)
        self.assertIsNotNone(saved_author)
        self.assertEqual(saved_author.name, "John Doe")

    def test_article_save_and_fetch(self):
        author = Author(name="John Doe")
        author.save()
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        article = Article(title="Test Title", content="Test Content", author_id=author.id, magazine_id=magazine.id)
        article.save()
        saved_article = Article.get_by_id(article.id)
        self.assertIsNotNone(saved_article)
        self.assertEqual(saved_article.title, "Test Title")

    def test_magazine_save_and_fetch(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        saved_magazine = Magazine.get_by_id(magazine.id)
        self.assertIsNotNone(saved_magazine)
        self.assertEqual(saved_magazine.name, "Tech Weekly")

    def test_article_author_name(self):
        author = Author(name="John Doe")
        author.save()
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        article = Article(title="Test Title", content="Test Content", author_id=author.id, magazine_id=magazine.id)
        article.save()
        self.assertEqual(article.author_name(), "John Doe")

    def test_author_articles(self):
        author = Author(name="John Doe")
        author.save()
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        article1 = Article(title="Test Title 1", content="Test Content 1", author_id=author.id, magazine_id=magazine.id)
        article1.save()
        article2 = Article(title="Test Title 2", content="Test Content 2", author_id=author.id, magazine_id=magazine.id)
        article2.save()
        self.assertEqual(author.articles(), ["Test Title 1", "Test Title 2"])

    def test_magazine_articles(self):
        author = Author(name="John Doe")
        author.save()
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        article1 = Article(title="Test Title 1", content="Test Content 1", author_id=author.id, magazine_id=magazine.id)
        article1.save()
        article2 = Article(title="Test Title 2", content="Test Content 2", author_id=author.id, magazine_id=magazine.id)
        article2.save()
        self.assertEqual(magazine.articles(), ["Test Title 1", "Test Title 2"])

    def test_magazine_contributors(self):
        author1 = Author(name="John Doe")
        author1.save()
        author2 = Author(name="Jane Smith")
        author2.save()
        magazine = Magazine(name="Tech Weekly", category="Technology")
        magazine.save()
        article1 = Article(title="Test Title 1", content="Test Content 1", author_id=author1.id, magazine_id=magazine.id)
        article1.save()
        article2 = Article(title="Test Title 2", content="Test Content 2", author_id=author2.id, magazine_id=magazine.id)
        article2.save()
        self.assertEqual(magazine.contributors(), ["John Doe", "Jane Smith"])

if __name__ == "__main__":
    unittest.main()


