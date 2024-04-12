import sqlite3

class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TableCreationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InsertError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class QueryError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def get_db():
    try:
        return sqlite3.connect(':memory:')
    except sqlite3.Error as e:
        raise DatabaseError(str(e))

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE movies (
                    year INTEGER,
                    title TEXT,
                    studios TEXT,
                    producers TEXT,
                    winner TEXT
                    )''')
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise TableCreationError(str(e))

def insert_movie(row, conn):
    try:
        c = conn.cursor()
        c.execute('''INSERT INTO movies (year, title, studios, producers, winner)
                     VALUES (?, ?, ?, ?, ?)''',
                  (row['year'], row['title'], row['studios'], row['producers'], row['winner']))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise InsertError(str(e))

def get_producer_data(producer_name, conn):
    try:
        c = conn.cursor()
        c.execute("SELECT year FROM movies WHERE producers = ? AND winner = 'yes'", (producer_name,))
        return c.fetchall()
    except sqlite3.Error as e:
        raise QueryError(str(e))

def get_winner_producers(conn):
    try:
        c = conn.cursor()
        c.execute('''SELECT producers
                              FROM movies
                              WHERE winner = 'yes'
                              GROUP BY producers
                              HAVING COUNT(*) > 1''')
        return c.fetchall()
    except sqlite3.Error as e:
        raise QueryError(str(e))
