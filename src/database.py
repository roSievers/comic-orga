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

    def comics(self, user_id=None):
        if user_id is None:
            comics = self.c.execute("select * from comics")
        else:
            query = \
            """select following.comic, comics.name, comics.link from following
               join comics on following.comic = comics.id
               where following.user= ? """

            comics = self.c.execute(query,user_id)
        for comic in comics:
            print(comic)

    def new_comic(self, name, link):
        query = "insert into comics (name, link) values (?, ?)"
        self.c.execute(query,(name,link))
        self.conn.commit()

    def new_user(self, name):
        # TODO: Generate password
        query = "insert into users (name) values ( ? ) "
        self.c.execute(query,name)
        self.conn.commit()

    def subscribe(self, user_id, comic_id):
        query = """insert into following (user, comic)
                   values (?, ?)"""
        self.c.execute(query,(user_id,comic_id))
        self.conn.commit()

    def new_page(self, comic_id, title, link, **data):
        timestamp = int(time.time())
        query = """insert into pages (comic, title, link, timestamp)
                   values (?, ?, ?, ?)"""

        page_id = self.c.execute(query,(comic_id, title, link, timestamp)).lastrowid
        for key, value in data.items():
            query = """insert into data (page, key, value)
                            values (?, ?, ?)"""
            print(query,(page_id, key, value))
            self.c.execute(query)

    def unread(self, comic_id, timestamp):
        query = """select id, title, link, timestamp from pages
                        where (timestamp >= ?)
                          and (comic = ?)"""
        pages = self.c.execute(query,(timestamp,comic_id))
        for page in pages:
            print(page)

    def page(self, page_id):
        query = f"""select (comic, title, link) from pages where id= ?"""
        self.c.execute(query,comic_id)
