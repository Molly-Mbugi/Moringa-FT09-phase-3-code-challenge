

from database.connection import get_db_connection

class Article:
    def __init__(self, title, content, author_id, magazine_id):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = None  # Initialize id attribute

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                       (self.title, self.content, self.author_id, self.magazine_id))
        self.id = cursor.lastrowid  # Set id attribute after insertion
        conn.commit()
        conn.close()

    def author_name(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM authors WHERE id = ?", (self.author_id,))
        author_name = cursor.fetchone()[0]  # Assuming name is the first column
        conn.close()
        return author_name

    @classmethod
    def get_by_id(cls, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return cls(title=row["title"], content=row["content"], author_id=row["author_id"], magazine_id=row["magazine_id"])

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        articles = []
        for row in rows:
            article = cls(title=row["title"], content=row["content"], author_id=row["author_id"], magazine_id=row["magazine_id"])
            article.id = row["id"]
            articles.append(article)
        return articles

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS articles")
        conn.commit()
        conn.close()

    










