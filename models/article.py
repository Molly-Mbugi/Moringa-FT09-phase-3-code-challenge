import sqlite3

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = value
    
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError("Content must be a string")
        self._content = value
    
    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Author ID must be an integer")
        self._author_id = value
    
    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Magazine ID must be an integer")
        self._magazine_id = value
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    def save(self):
        """ Save the Article object into the database. """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            sql = """
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid
        else:
            sql = """
                UPDATE articles
                SET title=?, content=?, author_id=?, magazine_id=?
                WHERE id=?
            """
            cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id, self.id))
        
        conn.commit()
        
        cursor.close()
        conn.close()
    
    def delete(self):
        """ Delete the Article object from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "DELETE FROM articles WHERE id=?"
        cursor.execute(sql, (self.id,))
        
        conn.commit()
        
        cursor.close()
        conn.close()
        

    @classmethod
    def get_by_id(cls, article_id):
        """ Retrieve an Article object by its ID from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "SELECT * FROM articles WHERE id=?"
        cursor.execute(sql, (article_id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not row:
            return None
        
        return cls(
            id=row["id"],
            title=row["title"],
            content=row["content"],
            author_id=row["author_id"],
            magazine_id=row["magazine_id"]
        )

    @classmethod
    def get_all(cls):
        """ Retrieve all Article objects from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = "SELECT * FROM articles"
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        articles = []
        for row in rows:
            article = cls(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                author_id=row["author_id"],
                magazine_id=row["magazine_id"]
            )
            articles.append(article)
        
        return articles

    @classmethod
    def drop_table(cls):
        """ Drop the articles table from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            DROP TABLE IF EXISTS articles;
        """
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        conn.close()








