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
    
    @classmethod
    def get_by_id(cls, magazine_id):
        """ Retrieve a Magazine object by its ID from the database. """
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

    @classmethod
    def get_all(cls):
        """ Retrieve all Magazine objects from the database. """
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
        
        return magazines

    @classmethod
    def delete_by_id(cls, magazine_id):
        """ Delete a magazine by its ID from the database. """
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

    @classmethod
    def drop_table(cls):
        """ Drop the magazines table from the database. """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            DROP TABLE IF EXISTS magazines;
        """
        cursor.execute(sql)
        conn.commit()
        
        cursor.close()
        conn.close()



