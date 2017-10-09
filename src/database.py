import sqlite3
from sanitize import sanitize, maybe, mapping
import time

import hashlib
import urllib.request

class Database:
    def __init__(self, filename="database.db"):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

    """Takes all data about a website and stores it. Will also download images
    found in data["img"] which is either a URL or a list of URLs."""
    def register_comic(self, comic_id, comic_url, data):
        # Download and store images
        file_type = data["img"].split(".")[-1]
        target_file = hashlib.sha256(comic_url.encode(  )).hexdigest() + "." + file_type
        with urllib.request.urlopen("https:"+data["img"]) as adress:
            with open(target_file , "wb") as f:
                f.write(adress.read())

        data["img"] = target_file
        title = data["title"]
        del data["title"]
        self.new_page(comic_id, title, comic_url, **data)

    @sanitize(None, maybe(int))
    def comics(self, user_id=None):
        if user_id is None:
            comics = self.c.execute("select * from comics")
        else:
            query = \
            f"""select following.comic, comics.name, comics.link from following
               join comics on following.comic = comics.id
               where following.user={user_id}"""

            comics = self.c.execute(query)
        for comic in comics:
            print(comic)

    @sanitize(None, str, str)
    def new_comic(self, name, link):
        query = f"insert into comics (name, link) values ('{name}', '{link}')"
        self.c.execute(query)
        self.conn.commit()

    @sanitize(None, str)
    def new_user(self, name):
        # TODO: Generate password
        query = f"insert into users (name) values ('{name}')"
        self.c.execute(query)
        self.conn.commit()

    @sanitize(None, int, int)
    def subscribe(self, user_id, comic_id):
        query = f"""insert into following (user, comic)
                    values ('{user_id}', '{comic_id}')"""
        self.c.execute(query)
        self.conn.commit()

    @sanitize(None, int, str, str, mapping(str, str))
    def new_page(self, comic_id, title, link, **data):
        timestamp = int(time.time())
        query = \
        f"""insert into pages (comic, title, link, timestamp)
           values ('{comic_id}', '{title}', '{link}', '{timestamp}')"""

        page_id = self.c.execute(query).lastrowid
        for key, value in data.items():
            query = f"""insert into data (page, key, value)
                            values ('{page_id}', '{key}', '{value}')"""
            print(query)
            self.c.execute(query)

    @sanitize(None, int, int)
    def unread(self, comic_id, timestamp):
        query = f"""select id, title, link, timestamp from pages
                        where (timestamp >= '{timestamp}')
                          and (comic = '{comic_id}')"""
        pages = self.c.execute(query)
        for page in pages:
            print(page)

    @sanitize(None, int)
    def page(self, page_id):
        query = f"""select (comic, title, link) from pages where id={page_id}"""
