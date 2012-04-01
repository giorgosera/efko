from app.handlers import base
from mongoengine.queryset import DoesNotExist
from app.model.video import *
from random import shuffle

class HomePageHandler(base.BaseHandler):
    '''
    Check user status and either load the home screen or the
    welcome page.
    '''
    def on_get(self):
        songs = [item for item in VideoItem.objects if not item.viewed]
        shuffle(songs)
        first_selection = songs.pop(0)
        for song in songs:
            if first_selection.title == song.title:
                second_selection = song
                break
        first_selection.flagged_as_seen()
        second_selection.flagged_as_seen() 
          
        return first_selection, second_selection
    
    def on_success(self, f, s):
        self.base_render("intro.html", first=f, second=s)
    
class VoteHandler(base.BaseHandler):

    def on_post(self):
        sid = self.get_argument("sid", None)
        vi = VideoItem.objects(id=sid).get()
        vi.upvote()

class SubmitCoverHandler(base.BaseHandler):
    def on_get(self):
        self.base_render("submit.html")
    
    def on_post(self):
        url = self.get_argument("url", None)
        title = self.get_argument("title", None)
        artist = self.get_argument("artist", None)
        genre = self.get_argument("genre", None)
        uploader = self.get_argument("uploader", None)
        
        vi = VideoItem()
        vi.url = url
        vi.title = title
        vi.artist = artist
        vi.genre = genre
        vi.uploader = uploader
        vi.save()