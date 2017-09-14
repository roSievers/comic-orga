
import sqlite3
from sanitize import sanitize
import time

class Database:
    def __init__(self, filename="database.db"):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

    def comics(self, user=None):
        if user is None:
            comics = self.c.execute("select * from comics")
        else:
            query = f"""select following.comic, comics.name, comics.link from following
                            join comics on following.comic = comics.id
                            where following.user={user}"""
            comics = self.c.execute(query)
        for comic in comics:
            print(comic)

    @sanitize
    def new_comic(self, name, link):
        query = f"insert into comics (name, link) values ('{name}', '{link}')"
        self.c.execute(query)
        self.conn.commit()

    @sanitize
    def new_user(self, name):
        # TODO: Generate password
        query = f"insert into users (name) values ('{name}')"
        self.c.execute(query)
        self.conn.commit()

    def subscribe(self, user_id, comic_id):
        query = f"insert into following (user, comic) values ('{user_id}', '{comic_id}')"
        self.c.execute(query)
        self.conn.commit()

    def new_page(self, comic_id, title, link, **data):
        timestamp = int(time.time())
        query = f"""insert into pages (comic, title, link, timestamp)
                        values ('{comic_id}', '{title}', '{link}', '{timestamp}')"""
        page_id = self.c.execute(query).lastrowid
        for key, value in data.items():
            query = f"""insert into data (page, key, value)
                            values ('{page_id}', '{key}', '{value}')"""
            print(query)
            self.c.execute(query)

    def unread(self, comic_id, timestamp):
        query = f"""select id, title, link, timestamp from pages
                        where (timestamp >= '{timestamp}')
                          and (comic = '{comic_id}')"""
        pages = self.c.execute(query)
        for page in pages:
            print(page)

    def page(self, page_id):
        query = f"""select (comic, title, link) from pages where id={page_id}"""

db = Database()

db.comics()
