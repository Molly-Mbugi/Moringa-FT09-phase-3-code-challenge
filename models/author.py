import sqlite3

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name  # Using the setter

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
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
        if self.id is None:
            raise ValueError("Cannot delete an author with no ID.")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM authors WHERE id=?", (self.id,))

        conn.commit()
        cursor.close()
        conn.close()
    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [cls(id=row["id"], name=row["name"]) for row in rows]
    @classmethod
    def delete_by_id(cls, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM authors WHERE id=?", (author_id,))

        conn.commit()
        cursor.close()
        conn.close()



















    