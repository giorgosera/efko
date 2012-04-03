from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.video import *

class ListSongsHandler(base.BaseHandler):
    '''
    Lists all Youtube videos
    '''
    def on_get(self):
        songs = [song for song in VideoItem.objects]
        size = len(songs)
        songs1 = songs[:size/2]
        songs2 = songs[size/2:]
        self.base_render("songlist.html", songs1=songs1, songs2=songs2)    
        
    def on_post(self):
        sid = self.get_argument("sid", None)
        VideoItem.objects(id=sid).delete()