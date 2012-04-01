from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.video import *

class PopulateDummyHandler(base.BaseHandler):
    '''
    Populates the database with dummy Youtube videos
    '''
    def on_post(self):
        i = 0
        while (i<2):
            url = raw_input("Song's url")
            title = raw_input("Song's title")
            artist = raw_input("Who's the artist?")
            uploader = raw_input("Who's the uploader?")
            genre = raw_input("What's the genre?")
            
            vi = VideoItem()
            vi.url = url
            vi.title = title
            vi.artist = artist
            vi.uploader = uploader
            vi.genre = genre
            try:
                vi.save(safe=True)
            except Exception, e:
                print e
            i+=1