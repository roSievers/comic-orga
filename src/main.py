
from database import Database
import scrapper

database = Database()

xkcd = scrapper.XkcdParser(1, "http://xkcd.com/1524")

xkcd.run(database)
