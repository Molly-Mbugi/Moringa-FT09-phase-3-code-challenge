import sqlite3
from database.connection import get_db_connection

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name 

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        if hasattr(self, '_name'):
            raise AttributeError("Cannot modify name after it has been set")
        self._name = value

    def __repr__(self):
        return f'<Author {self.name}>'

    def save(self):
        """ Save or update the Author object in the database. """
        conn = get_db_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))

        conn.commit()
        cursor.close()
        conn.close()

    def delete(self):
        """ Delete the Author object from the database. """
        if self.id is None:
            raise ValueError("Cannot delete an author with no ID.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM authors WHERE id=?", (self.id,))

        conn.commit()
        cursor.close()
        conn.close()

    def articles(self):
        """ Retrieve articles authored by this author. """
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT articles.title
            FROM articles
            LEFT JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        """
        cursor.execute(sql, (self._id,))
        articles = cursor.fetchall()

        cursor.close()
        conn.close()

        return [article["title"] for article in articles] if articles else []

    @classmethod
    def get_by_id(cls, author_id):
        """ Retrieve an Author object by their ID from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM authors WHERE id=?"
        cursor.execute(sql, (author_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return cls(id=row["id"], name=row["name"])

    @classmethod
    def get_all(cls):
        """ Retrieve all authors from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [cls(id=row["id"], name=row["name"]) for row in rows]

    @classmethod
    def delete_by_id(cls, author_id):
        """ Delete an author by their ID from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM authors WHERE id=?", (author_id,))

        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def drop_table(cls):
        """ Drop the authors table from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DROP TABLE IF EXISTS authors;"
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()





















    