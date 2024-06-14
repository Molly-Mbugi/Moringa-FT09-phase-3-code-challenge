import sqlite3

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

class Magazine:
    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

        if self.id is None:
            self.save()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    def save(self):
        """ Save the Magazine object into the database. """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if self.id is None:
                sql = """
                    INSERT INTO magazines (name, category)
                    VALUES (?, ?)
                """
                cursor.execute(sql, (self.name, self.category))
                self.id = cursor.lastrowid
            else:
                sql = """
                    UPDATE magazines
                    SET name=?, category=?
                    WHERE id=?
                """
                cursor.execute(sql, (self.name, self.category, self.id))
            
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # Store in the class-level dictionary
            Magazine.all[self.id] = self
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @classmethod
    def get_by_id(cls, magazine_id):
        """ Retrieve a Magazine object by its ID from the database. """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM magazines WHERE id=?"
            cursor.execute(sql, (magazine_id,))
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not row:
                return None
            
            return cls(
                id=row["id"],
                name=row["name"],
                category=row["category"]
            )
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @classmethod
    def get_all(cls):
        """ Retrieve all Magazine objects from the database. """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM magazines"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            magazines = []
            for row in rows:
                magazine = cls(
                    id=row["id"],
                    name=row["name"],
                    category=row["category"]
                )
                magazines.append(magazine)
                Magazine.all[row["id"]] = magazine
            
            return magazines
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @classmethod
    def delete_by_id(cls, magazine_id):
        """ Delete a magazine by its ID from the database. """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM magazines WHERE id=?"
            cursor.execute(sql, (magazine_id,))
            
            conn.commit()
            
            cursor.close()
            conn.close()

            # Remove from the class-level dictionary if exists
            if magazine_id in cls.all:
                del cls.all[magazine_id]
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    @classmethod
    def drop_table(cls):
        """ Drop the magazines table from the database. """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = """
                DROP TABLE IF EXISTS magazines;
            """
            cursor.execute(sql)
            conn.commit()
            
            cursor.close()
            conn.close()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    
    def articles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT articles.title
                FROM articles
                LEFT JOIN magazines
                ON articles.magazine_id = magazines.id
                WHERE magazines.id = ?
            """
            cursor.execute(query, (self.id,))
            articles = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [article["title"] for article in articles] if articles else []
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def contributors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = """
                SELECT authors.name
                FROM authors
                LEFT JOIN articles
                ON authors.id = articles.author_id
                LEFT JOIN magazines
                ON articles.magazine_id = magazines.id
                WHERE magazines.id = ?
            """
            cursor.execute(sql, (self.id,))
            contributors = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [contributor["name"] for contributor in contributors] if contributors else []
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def article_titles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = """
                SELECT articles.title
                FROM articles
                WHERE articles.magazine_id = ?
            """
            cursor.execute(sql, (self.id,))
            article_titles = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [article_title["title"] for article_title in article_titles] if article_titles else []
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def contributing_authors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            sql = """
                SELECT authors.name
                FROM authors
                LEFT JOIN articles 
                ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING COUNT(articles.id) > 2
            """
            cursor.execute(sql, (self.id,))
            contributing_authors = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return [contributing_author["name"] for contributing_author in contributing_authors] if contributing_authors else []
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    mag = Magazine(name="Tech Monthly", category="Technology")
    print(mag)

    all_mags = Magazine.get_all()
    print(all_mags)



