# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 08:21:45 2017

@author: Adeptus Alricus
"""

from lxml import html
import requests
import urllib.request
import urllib.parse


#href = tree.xpath('//a[@rel="next"]')[0].attrib["href"]
#with urllib.request.urlopen("https:"+img) as adress:
#    with open('ears.png' , "wb") as f:
#        f.write(adress.read())

class PageParser():
    def __init__(self, comic_id, start_url):
        self.comic_id = comic_id
        self.current_url = start_url

    def run(self, database):
        while True:
            next_url = self.extract_one(database)
            if self.current_url == next_url:
                break
            self.current_url= next_url

    def extract_one(self, database):
        page = requests.get(self.current_url)
        tree = html.fromstring(page.content)

        data = self.extract_information(tree)
        print(data)
        if "img" in data:
            database.register_comic(self.comic_id, self.current_url, data)

        return urllib.parse.urljoin(self.current_url, data["href_next"])

class XkcdParser(PageParser):
    def extract_information(self, tree):
        images = tree.xpath('//div[@id="comic"]/img')
        if len(images) != 1:
            return { "href_next" : tree.xpath('//a[@rel="next"]')[0].attrib["href"] }

        comic = images[0]

        if not ("alt" in comic.attrib and "title" in comic.attrib):
            return { "href_next" : tree.xpath('//a[@rel="next"]')[0].attrib["href"] }            

        return { "title"     : comic.attrib["alt"]
               , "alt"       : comic.attrib["title"]
               , "img"       : comic.attrib["src"]
               , "href_next" : tree.xpath('//a[@rel="next"]')[0].attrib["href"]
               }
